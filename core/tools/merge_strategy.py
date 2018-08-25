__author__ = 'zhangchuan'

import random
import time
import new
import uuid


class Merger(object):
    def __init__(self):
        self.biz_name = ''
        self.context = {}
        self.params = {}
        self.result = None

    def merge(self, biz_module):
        raise Exception('not implemented yet')

    def handle_module(self, biz_module):
        handler = biz_module.get_handler()
        return handler(self.get_context(), **self.get_params())

    def set_biz_name(self, biz_name):
        self.biz_name = biz_name

    def get_biz_name(self):
        return self.biz_name

    def set_context(self, context):
        self.context = context

    def get_context(self):
        return self.context

    def set_params(self, params):
        self.params = params

    def get_params(self):
        return self.params

    def get_result(self):
        return self.result


class MergeStrategy(object):
    def __init__(self):
        pass

    def create_merger(self):
        merger = Merger()
        setattr(merger, 'merge', new.instancemethod(self.merge_func, merger, None))
        setattr(merger, 'get_result', new.instancemethod(self.get_result_func, merger, None))
        return merger

    @staticmethod
    def merge_func(merger, biz_module):
        pass

    @staticmethod
    def get_result_func(merger):
        return merger.result


class Sequence(MergeStrategy):
    def __init__(self):
        MergeStrategy.__init__(self)

    @staticmethod
    def merge_func(merger, biz_module):
        merger.handle_module(biz_module)
        return True


class FirstResult(MergeStrategy):
    def __init__(self):
        MergeStrategy.__init__(self)

    @staticmethod
    def merge_func(merger, biz_module):
        result = merger.handle_module(biz_module)
        if result is not None:
            merger.result = result
        return result is None


class Pipeline(MergeStrategy):
    def __init__(self):
        MergeStrategy.__init__(self)

    def create_merger(self):
        merger = MergeStrategy.create_merger(self)
        merger.result_key = '_pipeline_result'
        return merger

    @staticmethod
    def merge_func(merger, biz_module):
        result = merger.handle_module(biz_module)
        merger.result = result
        merger.params[merger.result_key] = result
        return True

    @staticmethod
    def get_result_func(merger):
        del merger.params[merger.result_key]
        return merger.result


class LoggedPipeline(Pipeline):
    def __init__(self, config):
        Pipeline.__init__(self)
        self.config = config
        self.uuid = str(uuid.uuid1())

    def is_enabled(self):
        return self.config['enabled']

    def get_logger(self):
        return self.config['logger']

    def create_merger(self):
        merger = Pipeline.create_merger(self)
        merger.log_enabled = self.is_enabled()
        merger.logger = self.get_logger()
        merger.log_id = self.uuid
        return merger

    @staticmethod
    def merge_func(merger, biz_module):
        result = merger.handle_module(biz_module)
        merger.result = result
        merger.params[merger.result_key] = result
        context = merger.get_context()
        if merger.log_enabled(context):
            logger = merger.logger
            logger({
                'request_id': merger.log_id,
                'biz_module': biz_module.get_name(),
                'result': str(result)
            })
        return True


class Accumulator(MergeStrategy):
    def __init__(self):
        MergeStrategy.__init__(self)

    def create_merger(self):
        merger = MergeStrategy.create_merger(self)
        setattr(merger, 'accumulate', new.instancemethod(self.accumulate_func, merger, None))
        merger.first = True
        return merger

    @staticmethod
    def merge_func(merger, biz_module):
        result = merger.handle_module(biz_module)
        if merger.first:
            merger.result = result
            merger.first = False
        else:
            merger.accumulate(result)
        return True

    @staticmethod
    def accumulate_func(merger, result):
        merger.result += result


class DictAccumulator(Accumulator):
    def __init__(self):
        MergeStrategy.__init__(self)

    @staticmethod
    def accumulate_func(merger, result):
        for key, value in result.items():
            if value is None:
                merger.result[key] = None
            else:
                current = merger.result.get(key, 0)
                if current is not None:
                    merger.result[key] = current + value


class Random(MergeStrategy):
    def __init__(self):
        MergeStrategy.__init__(self)

    def create_merger(self):
        merger = MergeStrategy.create_merger(self)
        merger.modules = []
        return merger

    @staticmethod
    def merge_func(merger, biz_module):
        merger.modules.append(biz_module)
        return True

    @staticmethod
    def get_result_func(merger):
        handler_count = len(merger.modules)
        idx = random.randint(0, handler_count - 1)
        selected_module = merger.modules[idx]
        return merger.handle_module(selected_module)


class Profiled(MergeStrategy):
    def __init__(self, merge_strategy, log):
        MergeStrategy.__init__(self)
        self.merge_strategy = merge_strategy
        self.log = log

    def create_merger(self):
        if isinstance(self.merge_strategy, type):
            merge_strategy = object.__new__(self.merge_strategy)
            merge_strategy.__init__()
        else:
            merge_strategy = self.merge_strategy
        merger = merge_strategy.create_merger()
        merger.log = self.log
        wrapped_merge_func = self.create_handle_module_func(merger.handle_module)
        setattr(merger, 'handle_module', new.instancemethod(wrapped_merge_func, merger, None))
        return merger

    @staticmethod
    def create_handle_module_func(handle_module):
        def wrapped_func(merger, biz_module):
            start = time.time()
            result = handle_module(biz_module)
            end = time.time()
            elapsed = (end - start) * 1000
            module_name = biz_module.get_name()
            biz_name = merger.get_biz_name()
            merger.log({'%s@%s' % (module_name, biz_name): '%.2f' % elapsed})
            return result

        return wrapped_func
