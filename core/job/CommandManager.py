# -*- encoding: utf8 -*-

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
import env_loader
from core.log import getLogger
from job_command import JobCommand

logger = getLogger(__name__)
logger.debug('project_dir is [%s]' % env_loader.project_dir)


if __name__ == '__main__':

    from core import app, db
    app.config['DEBUG_TB_HOSTS'] = '127.0.0.1'
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.add_command('job', JobCommand)

    manager.run()
