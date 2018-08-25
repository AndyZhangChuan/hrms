# -*- encoding: utf8 -*-
__author__ = 'zhangchuan'

import inspect
import time, re, random, uuid, sys, os
from datetime import datetime
import threading
from functools import wraps

__name__ = "code_profiler"

import new

from core import app
from core.kafka.kafkalogging import LoggerGetter

from core.utils import utils
from core.utils.utils import local_ip
from core import log

topic_name = 'topic_code_profile'
kk_log = LoggerGetter.get_biz_logger(app.config['KAFKA_HOSTS_LIST'], topic_name)

all_module_names = set()
module_dir_names = {}

profile_local = threading.local()

def begin_code_profile(request):
    if not may_aspect():
        return False

    rand = random.randint(0, get_code_profile_ratio() - 1)
    if rand == 0:
        profile_local.__dict__['uuid'] = str(uuid.uuid1()).replace('-', '')
        profile_local.__dict__['codec'] = True
        profile_local.__dict__['url'] = request.path
        return True
    else:
        profile_local.__dict__['codec'] = False

    return False

def end_code_profile(request):
    if not may_aspect():
        return

    if getattr(profile_local, 'codec', False):
        profile_local.__dict__['uuid'] = ''
        profile_local.__dict__['codec'] = False
        profile_local.__dict__['url'] = ''

def profile_aspect(show_arg=None):
    def _profile_aspect(func, obj=None):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if obj:
                args = (obj,) + args

            # if profile_local.__dict__.get('codec', None) is None:
            #     begin_code_profile({})

            # and dice_round()
            if profile_local.__dict__.get('codec', False):
                ss = time.time()
                exec_val = func(*args, **kwargs)
                ee = time.time()
                # print profile_local.uuid, " total spent ", func, " , ", (ee - ss)
                log_func_exec((ee - ss), func, args, kwargs, show_arg)
                return exec_val
            else:
                exec_val = func(*args, **kwargs)
                return exec_val

        return wrapper
    return _profile_aspect

spaces_pattern = re.compile("[\n|\r|\t]")
def log_func_exec(exec_time, func, args, kwargs, show_arg=None):

    if show_arg is not None:
        kwargs = {}
        print_args = []
        for i in xrange(0, len(args)):
            if i in show_arg:
                print_args.append(args[i])
    else:
        print_args = args

    try:
        logging_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

        clz_name = ''
        co_varnames = func.func_code.co_varnames
        if co_varnames and len(co_varnames) > 0 and co_varnames[0] == 'self':
            # setattr(vv, meth_name, profile_aspect()(meth, vv))
            try:
                clz_name = args[0].__class__.__name__ + '.'
            except:
                pass

        la = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(profiler.project_id, logging_time, local_ip,
                                                    profile_local.__dict__.get('url', ''),
                                                    round(exec_time * 1000, 3),
                                                    profile_local.__dict__.get('uuid', ''),
                                                    func.__module__ + "." + clz_name + func.func_name,
                                                    re.sub(spaces_pattern, ' ', str(print_args)),
                                                    re.sub(spaces_pattern, ' ', str(kwargs)))
        kk_log.get_kk_log(topic_name).info(la)
    except:
        log.error("log_func_exec error: %s", utils.current_exception_info())

class MethodWrapper(object):

    method_patterns = set()

    def __init__(self, module_name, clazz_name, method_pattern):
        self.method_pattern = method_pattern
        self.clazz_name = clazz_name
        self.module_name = module_name
        self.mod = get_module(module_name)
        if self.mod is None:
            raise Exception("module_name %s", module_name, " do not exist ")

        self.method_patterns.add(build_pattern(module_name, clazz_name, method_pattern))

        self.aspect_clazzs = {}

        # {module.obj.method: {obj: origin_obj_method}, module.obj.method: {obj: origin_obj_method} }
        self.object_method_origin = {}

        # {module_clazz_method1: origin_func, module_clazz_method2: origin_func}
        self.clazz_method_origin = {}
        # {module_clazz1: origin_clazz, module_clazz2: origin_clazz}
        self.clazz_origin = {}

    def wrap_method(self):
        if not does_profile_switch_on() or not does_local_ip_matched():
            log.info('code_profile_switch is False or does_local_ip_matched is False')
            return

        log.info('start profile method for %s.%s pattern is %s', self.mod.__name__, self.clazz_name, self.method_pattern)

        self.__wrap_method_internal()

        # aspect functions that are imported classes and objects by from .. import
        imported_modules = []
        for na in all_module_names.copy():
            if na == self.mod.__name__ or get_module(na) is None:
                continue
            mo = get_module(na)
            imported_modules.append(na)
            # log.info("search imported clazz %s", na)

            for kk, vv in mo.__dict__.items():
                try:
                    if kk.startswith("__") or inspect.ismodule(vv):
                        continue
                    if inspect.isclass(vv) and vv in self.aspect_clazzs:
                        self.__wrap_other_clazz_method(kk, vv, mo)
                    else:
                        self.__wrap_other_object_method(kk, vv)
                except:
                    all_module_names.remove(na)
                    log.warn("%s error: %s", na, utils.current_exception_info())

        log.info("search imported module %s", str(imported_modules))
        log.info('end profile method for %s.%s pattern is %s', self.mod.__name__, self.clazz_name, self.method_pattern)

    def __wrap_method_internal(self):
        for k, v in self.mod.__dict__.items():
            try:
                if not inspect.isclass(v) or getattr(v, '__module__') != self.mod.__name__:
                    continue
                meta_dict = self.get_aspect_clazz_methods(k, v)
                if len(meta_dict) == 0:
                    continue

                meta_clazz = v
                for kk, meth in meta_clazz.__dict__.items():
                    if kk.startswith("__"):
                        continue

                    # meth = getattr(meta_clazz, kk)
                    meth_func = getattr(meta_clazz, kk)
                    # print '11 ', kk, ', \t ', type(meth), ' \t, ', type(meth_func)

                    if not is_function(meth) and not is_method(meth):
                        continue
                    func_name = kk
                    if func_name not in meta_dict:
                        continue

                    if str(type(meth)).find('staticmethod') > -1:
                        # setattr(meta_clazz, kk, profile_aspect()(meth_func, meta_clazz))
                        setattr(meta_clazz, kk, staticmethod(profile_aspect()(meth_func)))

                    elif str(type(meth)).find('function') > -1:
                        setattr(meta_clazz, kk, profile_aspect()(meth))
                    elif str(type(meth)).find('classmethod') > -1:
                        # setattr(meta_clazz, kk, profile_aspect()(getattr(meth_func, 'im_func'), meta_clazz))
                        setattr(meta_clazz, kk, classmethod(profile_aspect()(getattr(meth_func, 'im_func'))))
                    else:
                        setattr(meta_clazz, kk, profile_aspect()(meth_func))

                    log.info("code profile for method - %s.%s.%s", meta_clazz.__module__, meta_clazz, func_name)

                setattr(self.mod, k, meta_clazz)
                self.aspect_clazzs[v] = meta_dict
                self.clazz_origin[self.mod.__name__ + "." + k] = v
            except:
                log.error('first aspect module class %s error: %s', self.mod.__name__, utils.current_exception_info())

    def __wrap_other_clazz_method(self, kk, vv, mo):
        self.clazz_origin[mo.__name__ + "." + kk] = vv
        setattr(mo, kk, getattr(self.mod, kk))
        log.info("code profile for import clazz %s at %s", kk, mo.__name__)

    def __wrap_other_object_method(self, kk, vv):
        for clz, meths in self.aspect_clazzs.items():
            if not isinstance(vv, clz):
                continue
            for meth_name, meth in meths.items():
                method_full_name = clz.__module__ + "." + clz.__name__ + "." + meth_name
                if not self.does_match_method_aspect(method_full_name):
                    continue
                self.object_method_origin[method_full_name] = [vv, meth]
                co_varnames = meth.func_code.co_varnames
                if co_varnames and len(co_varnames) > 0 and co_varnames[0] == 'self':
                    setattr(vv, meth_name, profile_aspect()(meth, vv))
                else:
                    setattr(vv, meth_name, profile_aspect()(meth))
                log.info("code profile for imported object method %s at %s", meth_name, kk)
            break

    def get_aspect_clazz_methods(self, clazz_name, clazz):
        meta_dict = {}
        for k, clazz_function in clazz.__dict__.items():
            if k.startswith("__"):
                continue

            # clazz_function = getattr(clazz, k)
            if is_function(clazz_function) or is_method(clazz_function):
                clazz_func = getattr(clazz, k)
                method_full_name = self.mod.__name__ + "." + clazz_name + "." + clazz_func.func_name
                if self.does_match_method_aspect(method_full_name) and not is_inner_function(clazz_func):
                    meta_dict[k] = clazz_function
                    self.clazz_method_origin[method_full_name] = clazz_function
                    # print "code profile for method - ", method_full_name
                    # log.info("code profile for method - %s", method_full_name)
        return meta_dict

    def restore_method_aspect(self):
        log.info("try restore_module_clazz_method_aspect %s %s %s", self.mod.__name__, self.clazz_name, self.method_pattern)

        patt = build_pattern(self.mod.__name__, self.clazz_name, self.method_pattern)
        if patt in self.method_patterns:
            self.method_patterns.remove(patt)

        for k, original_func in self.clazz_method_origin.items():
            self.__restore_method_internal(patt, k, original_func)

        patt2 = build_pattern(self.mod.__name__, self.clazz_name)
        for kk, vv in self.clazz_origin.copy().items():
            self.__restore_clazz_other(patt2, kk, vv)

        for kkk, vvv in self.object_method_origin.copy().items():
            self.__restore_method_object(patt, kkk, vvv)

    def __restore_method_internal(self, patt, k, original_func):
        if re.match(patt, k):
            r_first_dot = k.rindex('.')
            func_name = k[r_first_dot + 1:]
            r_second_dot = str(k).rindex('.', 0, r_first_dot - 1)
            clz_name = k[r_second_dot + 1:r_first_dot]
            # setattr(self.mod, func_name, original_func)
            clz = getattr(self.mod, clz_name)
            setattr(clz, func_name, original_func)
            self.clazz_method_origin.pop(k)
            log.info("restore class method %s", k)

    def __restore_clazz_other(self, patt2, kk, vv):
        if re.match(patt2, kk):
            na = kk[0:kk.rindex('.')]
            clz_name = kk[kk.rindex('.') + 1:]
            mo = get_module(na)
            # setattr(mo, clz_name, self.clazz_origin.pop(kk))
            setattr(mo, clz_name, getattr(self.mod, clz_name))
            self.clazz_origin.pop(kk)
            log.info("restore imported class %s at %s", kk, mo.__name__)

    def __restore_method_object(self, patt, kkk, vvv):
        if re.match(patt, kkk):
            obj = vvv[0]
            meth = vvv[1]

            co_varnames = meth.func_code.co_varnames
            if co_varnames and len(co_varnames) > 0 and co_varnames[0] == 'self':
                nmeth = new.instancemethod(meth, obj, None)
                setattr(obj, meth.__name__, nmeth)
            else:
                setattr(obj, meth.__name__, meth)

            self.object_method_origin.pop(kkk)

            log.info("restore object method %s", kkk)

    def does_match_method_aspect(self, method_full_name):
        for patt in self.method_patterns:
            if re.match(patt, method_full_name):
                return True
        return False

class FunctionWrapper(object):

    function_patterns = set()

    # {func_pattern:{origin_func_name:origin_func...}}
    patt_funcs_dict = {}

    # {module.func1_name: origin_func, module.func2_name: origin_func }
    module_func_origin = {}
    # {other_mod_name: origin_func}
    other_module_func_origin = {}

    def __init__(self, module_name, function_pattern):
        self.module_name = module_name
        self.function_pattern = function_pattern
        self.mod = get_module(module_name)
        try:
            if self.mod is None:
                import importlib
                importlib.import_module(module_name)
                self.mod = get_module(module_name)

        except:
            log.error('try to import %s error: %s', module_name, utils.current_exception_info())

        if self.mod is None:
            raise Exception("module_name %s do not exist ", module_name)

        self.function_patterns.add(build_pattern(module_name, function_pattern))

    def wrap_function(self):
        if not does_profile_switch_on() or not does_local_ip_matched():
            log.info('code_profile_switch is False or does_local_ip_matched is False')
            return

        log.info('start profile method for %s pattern is %s', self.mod.__name__, self.function_pattern)

        for k, v in self.mod.__dict__.items():
            self.__wrap_function_internal(k, v)

        # aspect functions that are imported by from .. import
        imported_modules = []
        for na in all_module_names.copy():
            mo = get_module(na)
            if mo is None:
                continue
            imported_modules.append(na)

            self.__wrap_other_function(mo)

        log.info("search imported module %s", str(imported_modules))
        log.info('end profile method for %s pattern is %s', self.mod.__name__, self.function_pattern)

    def __wrap_function_internal(self, k, v):
        try:
            if k.startswith("__"):
                return
            if inspect.isfunction(v) and getattr(v, '__module__') == self.mod.__name__:
                function_full_name = self.mod.__name__ + "." + v.func_name
                if self.does_match_function_aspect(function_full_name) and not is_inner_function(v):
                    setattr(self.mod, k, profile_aspect()(v))
                    self.module_func_origin[function_full_name] = v
                    log.info("code profile for function - %s", function_full_name)
        except:
            log.error('first aspect module %s error: %s', self.mod.__name__, utils.current_exception_info())

    def add_wrapped_func(self, matched_patt, origin_full_func_name, origin_func):
        func_set = self.patt_funcs_dict.get(matched_patt, None)
        if func_set is None:
            func_set = {}
            self.patt_funcs_dict[matched_patt] = func_set
        func_set[origin_full_func_name] = origin_func

    def __wrap_other_function(self, mo):
        try:
            mo_name = mo.__name__
            self_mod_name = self.mod.__name__

            if mo_name == self_mod_name:
                return

            for kk, vv in mo.__dict__.items():
                if kk.startswith("__"):  # or not inspect.ismodule(vv)
                    continue

                full_func_name = "%s.%s" % (mo_name, kk)

                if inspect.ismodule(vv) and vv is self.mod:  # inspect.ismodule(vv) and
                    self.module_func_origin[full_func_name] = vv
                    setattr(mo, kk, self.mod)
                    self.add_wrapped_func('__mod_match__', full_func_name, vv)
                    log.info("other code profile for import as %s at %s", kk, mo_name)
                elif inspect.isfunction(vv):
                    vv_mo_name = vv.__module__
                    matched_patt = self.does_match_function_aspect(vv_mo_name + '.' + kk)
                    if not matched_patt:
                        continue
                    # self.module_func_origin[full_func_name] = vv

                    setattr(mo, kk, profile_aspect()(vv))
                    self.add_wrapped_func(matched_patt, full_func_name, vv)
                    log.info("other code profile for from import %s at %s", full_func_name, mo_name)
        except:
            all_module_names.remove(mo.__name__)
            log.warn("%s error: %s", mo.__name__, utils.current_exception_info())


    def restore_function_aspect(self):
        log.info("try restore_module_clazz_method_aspect %s %s", self.mod.__name__, self.function_pattern)
        patt = build_pattern(self.mod.__name__, self.function_pattern)
        if patt in self.function_patterns:
            self.function_patterns.remove(patt)

        for func_name, v in self.module_func_origin.copy().items():
            if re.match(patt, func_name):
                self.__reset_func(func_name, v)
                self.module_func_origin.pop(func_name)
                log.info("restore module function %s", func_name)

        matched_funcs = self.patt_funcs_dict.get(patt, {})
        for original_func_name, original_func in matched_funcs.copy().items():
            self.__reset_func(original_func_name, original_func)
            matched_funcs.pop(original_func_name)
            log.info("restore other module function %s", original_func_name)

        matched_mods = self.patt_funcs_dict.get('__mod_match__', {})
        for original_func_name2, original_mod in matched_mods.copy().items():
            self.__reset_func(original_func_name2, original_mod)
            matched_mods.pop(original_func_name2)
            log.info("restore other module's mod %s", original_func_name2)


    def __reset_func(self, original_func_name, original_func):
        mod_name = original_func_name[0:original_func_name.rindex('.')]
        func_name = original_func_name[original_func_name.rindex('.') + 1:]
        func_mod = get_module(mod_name)
        setattr(func_mod, func_name, original_func)

    def does_match_function_aspect(self, function_full_name):
        for patt in self.function_patterns.copy():
            if re.match(patt, function_full_name):
                return patt
        return None

class CodeProfiler(object):

    method_wrappers = {}
    function_wrappers = {}
    searched_dirs = set()

    def __init__(self):
        self.project_id = '0'

    def set_project_id(self, project_id):
        self.project_id = project_id

    def __reload_all(self):
        log.info("__reload_all is called")
        for patt, mw in self.method_wrappers:
            mw.wrap_method()

        for patt2, fw in self.function_wrappers:
            fw.wrap_function()

    def __unload_all(self):
        log.info("__unload_all is called")
        for patt, mw in self.method_wrappers:
            mw.restore_method_aspect()

        for patt2, fw in self.function_wrappers:
            fw.restore_function_aspect()

    '''
     example: profile_module_class('aa.bb', '*', 'test_profile*')
    '''
    def profile_class_method(self, module_name, clazz_name, method_pattern):
        try:
            if not does_local_ip_matched():
                return
            patt = build_pattern(module_name, clazz_name, method_pattern)

            if patt in self.method_wrappers:
                mw = self.method_wrappers[patt]
                mw.restore_method_aspect()
                self.method_wrappers.pop(patt)

            mw = MethodWrapper(module_name, clazz_name, method_pattern)
            mw.wrap_method()
            self.method_wrappers[patt] = mw
        except:
            log.error("profile_class_method error: %s", utils.current_exception_info())

    '''
     example: profile_module_function('aa.bb', 'test*')
    '''
    def profile_module_function(self, module_name, function_pattern):
        try:
            if not does_local_ip_matched():
                return
            patt = build_pattern(module_name, function_pattern)

            if patt in self.function_wrappers:
                fw = self.function_wrappers[patt]
                fw.restore_function_aspect()
                self.function_wrappers.pop(patt)
            fw = FunctionWrapper(module_name, function_pattern)
            fw.wrap_function()
            self.function_wrappers[patt] = fw
        except:
            log.error("profile_module_function error: %s", utils.current_exception_info())

    def reload_module_functions(self, current_funcs, new_funcs):
        try:
            if not does_local_ip_matched():
                return
            # in current_funcs, but not in new_funcs, need to restore profile
            diff_restore = list(set(current_funcs).difference(set(new_funcs)))
            for aa in diff_restore:
                arr = str(aa).split(',')
                patt = build_pattern(arr[0], arr[1])
                if patt in self.function_wrappers:
                    fw = self.function_wrappers[patt]
                    fw.restore_function_aspect()
                    self.function_wrappers.pop(patt)

                    if aa in new_funcs:
                        new_funcs.remove(aa)

            # not in current_funcs, but in new_funcs, need to add profile
            # diff_profile = list(set(new_funcs).difference(set(current_funcs)))
            for aa in new_funcs:
                arr = str(aa).split(',')
                self.profile_module_function(arr[0], arr[1])
        except:
            log.error('reload_module_functions %s %s error: %s', str(current_funcs), str(new_funcs), utils.current_exception_info())

    def reload_class_methods(self, current_meths, new_meths):
        try:
            if not does_local_ip_matched():
                return
            # in current_funcs, but not in new_funcs, need to restore profile
            diff_restore = list(set(current_meths).difference(set(new_meths)))
            for aa in diff_restore:
                arr = str(aa).split(',')
                patt = build_pattern(arr[0], arr[1], arr[2])
                if patt in self.method_wrappers:
                    mw = self.method_wrappers[patt]
                    mw.restore_method_aspect()
                    self.method_wrappers.pop(patt)

                    if aa in new_meths:
                        new_meths.remove(aa)

            # not in current_funcs, but in new_funcs, need to add profile
            # diff_profile = list(set(new_meths).difference(set(current_meths)))
            for aa in new_meths:
                arr = str(aa).split(',')
                self.profile_class_method(arr[0], arr[1], arr[2])
        except :
            log.info("reload_class_methods %s , %s error: %s ", str(current_meths), str(new_meths), utils.current_exception_info())


    def search_all_module_from_config(self, curr_dir, new_dir):
        self.search_all_module(new_dir)

    def search_all_module(self, top_dirs):
        if not does_local_ip_matched():
            return
        ts = top_dirs.split(',')
        for top_dir in ts:
            self.__search_all_module(top_dir)

    def __search_all_module(self, top_dir):
        if top_dir is None or top_dir == '' or not does_profile_switch_on() or top_dir in self.searched_dirs:
            return

        reload_num = 0
        if top_dir.endswith('.reload'):
            reload_num = 1
            top_dir = top_dir[0:-7]

        if top_dir.endswith('.unload'):
            reload_num = 2
            top_dir = top_dir[0:-7]

        try:
            log.info("os.getcwd() is %s, top_dir is %s, ip is %s", os.getcwd(), top_dir, utils.local_ip)

            curr_real_path = os.path.realpath(__file__)
            work_dir = curr_real_path[0:curr_real_path.find('/core/profile')]

            log.info("work_dir is %s, os.path.dirname(__file__) is %s, %s", work_dir, os.path.dirname(__file__), curr_real_path)

            self.__find_sub_modules(work_dir, top_dir)

            self.searched_dirs.add(top_dir)
            log.info("all_module_names size is %s", len(all_module_names))

            if reload_num == 1:
                self.__reload_all()

            if reload_num == 2:
                self.__unload_all()

        except:
            log.info("search_all_module %s error: %s", top_dir, utils.current_exception_info())

    def __find_sub_modules(self, work_dir, top_dir):

        ww = work_dir + "/" + top_dir
        if os.path.isfile(ww):
            print 'ww is ', ww
            self.__add_module_by_file(ww)
            return

        try:
            for sub in os.listdir(ww):
                ss = top_dir + '/' + sub
                www = work_dir + '/' + ss
                if os.path.isfile(www):
                    module_name = self.__add_module_by_file(ss)
                    mods = module_dir_names.get(top_dir, None)
                    if mods is None:
                        mods = list()
                        module_dir_names[top_dir] = mods
                    if module_name:
                        mods.append(module_name)

                else:
                    # print 'work_dir is ', work_dir, ' subdir is ', ss

                    self.__find_sub_modules(work_dir, ss)
        except:
            log.error("work through %s error: %s", ww, utils.current_exception_info())

        print 'module names of ', top_dir, ' is ', module_dir_names[top_dir]

    def __add_module_by_file(self, ss):
        if ss.endswith('.py') and not ss.endswith('__.py'):  # not sub.startswith("__") and
            ss = ss[0:-3].replace('/', '.')
            while ss.startswith("."):
                ss = ss[1:]
            all_module_names.add(ss)
            return ss
        return None



def get_module(module_name):
    if module_name in sys.modules:
        return sys.modules[module_name]
    return None

def is_inner_function(func):
    return func.func_name == 'profile_aspect' or func.func_code.co_filename.find('code_profiler') > -1

def build_pattern(module, clazz_or_func, method=None):
    patt = module + "\." + clazz_or_func
    if method:
        patt += "\." + method
    return patt

def does_profile_switch_on():
    return app.config.get('CODE_PROFILE_SWITCH', False)

def does_local_ip_matched():
    matching_ip = app.config.get('CODE_PROFILE_MATCH_IP', '__no__')
    return re.match(matching_ip, utils.local_ip)

def get_code_profile_ratio():
    return app.config.get('CODE_PROFILE_RATIO', 0)

def is_function(func):
    return str(type(func)).find('function') > -1

def is_method(func):
    return str(type(func)).find('method') > -1

def may_aspect():
    return does_profile_switch_on() and get_code_profile_ratio() > 0 and does_local_ip_matched()

profiler = CodeProfiler()

