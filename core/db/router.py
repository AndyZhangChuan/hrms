# -*- encoding: utf8 -*-
from functools import partial
import logging
import threading
from flask.ext.sqlalchemy import SQLAlchemy, get_state
import sqlalchemy.orm as orm
from sqlalchemy.orm.session import Session as SessionBase

__author__ = 'zhangchuan'

log = logging.getLogger(__name__)
read_or_write = threading.local()


class AutoRouteSession(orm.Session):
    def _init_table_binds(self):
        result = {}
        binds = [None] + list(self.app.config.get('SQLALCHEMY_BINDS') or ())
        for bind in binds:
            tables = self.db.get_tables_for_bind(bind)
            result.update(dict((table, bind) for table in tables))
        return result

    def _init_db_map(self):
        result = {'hrms': []}
        binds = self.app.config['SQLALCHEMY_BINDS'] or []
        slave_key = "_slave"
        for k in binds:
            if slave_key not in k:
                result[k] = []

        for k in binds:
            if slave_key in k:
                p = k.find(slave_key)
                db_name = k[0:p]
                if db_name in result:
                    result[db_name].append(k)
                else:
                    result[db_name] = [k]
        return result

    def __init__(self, db, autocommit=False, autoflush=False, **options):
        self.app = db.get_app()
        self.db = db
        self.last_db_config = None
        bind = options.pop('bind', None) or db.engine
        SessionBase.__init__(self, autocommit=autocommit, autoflush=autoflush,
                             bind=bind,
                             binds=db.get_binds(self.app), **options)

        self.table_binds = self._init_table_binds()
        self.db_map = self._init_db_map()

    def get_bind(self, mapper=None, clause=None):
        try:
            state = get_state(self.app)
        except (AssertionError, AttributeError, TypeError) as err:
            log.info("Unable to get Flask-SQLAlchemy configuration. Outputting default bind. Error:" + err)
            return orm.Session.get_bind(self, mapper, clause)

        # If there are no binds configured, connect using the default SQLALCHEMY_DATABASE_URI
        if state is None or not self.app.config['SQLALCHEMY_BINDS']:
            if not self.app.debug:
                log.debug(
                    "Connecting -> DEFAULT. Unable to get Flask-SQLAlchemy bind configuration. Outputting default bind.")
            return orm.Session.get_bind(self, mapper, clause)

        has_bind = read_or_write.__dict__.has_key('read_or_write')
        if has_bind and read_or_write.__dict__['read_or_write'] == 'read':

            if 'read_type' in read_or_write.__dict__ and read_or_write.__dict__['read_type'] == 'force_read':
                bind_key = read_or_write.__dict__['bind_key']
                force_db_name = read_or_write.__dict__['force_db_name']
                mapper_db_name = self.get_dbname(mapper, clause)
                if mapper_db_name == bind_key:
                    # 若强制指定的从库，则走指定的从库
                    db_name = force_db_name
                else:
                    db_name = mapper_db_name
            else:
                db_name = self.get_dbname(mapper, clause)

            if len(self.db_map[db_name]) == 0:
                # 抛异常,@read不能没有_slave_
                raise Exception('请配置从库:' + db_name)
                pass

            slave_for_read = self.get_slave(db_name)
            return state.db.get_engine(self.app, bind=slave_for_read)
        else:
            if mapper is not None:
                info = getattr(mapper.mapped_table, 'info', {})
                bind_key = info.get('bind_key')
                if bind_key is not None:
                    return state.db.get_engine(self.app, bind=bind_key)
            return SessionBase.get_bind(self, mapper, clause)

    def get_dbname(self, mapper, clause):
        if mapper is not None:
            info = getattr(mapper.mapped_table, 'info', {})
            bind_key = info.get('bind_key')
            if bind_key:
                return bind_key
        if clause is not None:
            from sqlalchemy.sql import util
            is_match = False
            for t in util.find_tables(clause, include_crud=True):
                # print t,'------------',self.table_dbname_map
                if t in self.table_binds:
                    is_match = True
                    dn = self.table_binds[t];
                    break
            if is_match:
                return dn if dn is not None else "hrms"

        if read_or_write.__dict__.has_key('db_name') and read_or_write.__dict__['db_name'] is not None:
            db_name = read_or_write.__dict__['db_name']
            print '---------------@read(' + str(db_name) + ') has deprecated，you can easy use @read()----------'
            if db_name:
                return db_name

        return "hrms"

    def get_slave(self, db_name):
        uuid = read_or_write.__dict__['uuid']
        uuid_hash = hash(uuid)
        slave_len = len(self.db_map[db_name])
        slave_to_read_idx = uuid_hash % slave_len
        slave_to_read = self.db_map[db_name][slave_to_read_idx]
        return slave_to_read


class AutoRouteSQLAlchemy(SQLAlchemy):
    def __init__(self, app=None,
                 use_native_unicode=True,
                 session_options=None):
        SQLAlchemy.__init__(self, app, use_native_unicode, session_options)

    def create_scoped_session(self, options=None):
        """Helper factory method that creates a scoped session."""
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(AutoRouteSession, self, **options), scopefunc=scopefunc
        )
