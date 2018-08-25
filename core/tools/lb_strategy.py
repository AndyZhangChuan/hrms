__author__ = 'zhangchuan'

import random


class LoadBalanceStrategy:
    def __init__(self):
        pass

    def select_host(self, hosts, **options):
        pass


class RandomStrategy(LoadBalanceStrategy):
    def select_host(self, hosts, **options):
        rand = random.randint(0, len(hosts) - 1)
        return hosts[rand]


class WeightedStrategy(LoadBalanceStrategy):
    @staticmethod
    def _check_param(hosts, options):
        if 'weights' not in options:
            raise Exception('no weights in options')
        weights = options['weights']
        if len(weights) != len(hosts):
            raise Exception('weight count does not match host count')
        # eliminate below-zero weights
        for i in range(0, len(weights)):
            if weights[i] < 0:
                weights[i] = 0
        # if all weights are 0, change them into 1 to prevent crash
        if not any(options['weights']):
            options['weights'] = map(lambda w: 1, options['weights'])

    @staticmethod
    def _select_host(hosts, options):
        weights = options['weights']
        weight_sum = sum(weights)
        weights = map(lambda x: float(x) / weight_sum, weights)
        rand = random.random()
        weight_sum = 0
        for host, weight in zip(hosts, weights):
            weight_sum += weight
            if weight_sum > rand:
                return host, options

    def select_host(self, hosts, **options):
        self._check_param(hosts, options)
        return self._select_host(hosts, options)


class AdjustWeightStrategy(WeightedStrategy):
    @staticmethod
    def _check_param(hosts, options):
        if 'adjust_weights' not in options:
            raise Exception('no adjust weights in options')
        WeightedStrategy._check_param(hosts, options)

    def select_host(self, hosts, **options):
        self._check_param(hosts, options)
        adjust_weights = options['adjust_weights']
        for host in hosts:
            if host not in adjust_weights:
                adjust_weights[host] = 1
        weights = options['weights']
        options['weights'] = map(lambda h, w: w * adjust_weights[h], hosts, weights)
        WeightedStrategy._check_param(hosts, options)
        return WeightedStrategy._select_host(hosts, options)


class ConfigurableWeightStrategy(WeightedStrategy):
    @staticmethod
    def _check_param(hosts, options):
        if 'weight_config' not in options:
            raise Exception('weight_config not in options')
        if 'use_weight_config' not in options or options['use_weight_config'] is None:
            if 'default' not in options['weight_config']:
                raise Exception('no option selected')
            else:
                options['use_weight_config'] = 'default'
        else:
            use_weight_config = options['use_weight_config']
            if hasattr(use_weight_config, '__call__'):
                use_weight_config = use_weight_config()
                options['use_weight_config'] = use_weight_config
            if use_weight_config not in options['weight_config']:
                raise Exception('selected option not exist')

    def select_host(self, hosts, **options):
        self._check_param(hosts, options)
        use_weight_config = options['use_weight_config']
        weight_config = options['weight_config'][use_weight_config]
        filtered_hosts = []
        weights = []

        for host in hosts:
            if host not in weight_config:
                continue
            filtered_hosts.append(host)
            weights.append(weight_config[host])

        options['weights'] = weights
        return filtered_hosts, options


class CompositeStrategy(LoadBalanceStrategy):
    def __init__(self):
        self.strategies = []
        LoadBalanceStrategy.__init__(self)

    def select_host(self, hosts, **options):
        result = hosts
        for strategy in self.strategies:
            result, options = strategy.select_host(result, **options)
        return result


random_strategy = RandomStrategy()

default_strategy = CompositeStrategy()
default_strategy.strategies.append(ConfigurableWeightStrategy())
default_strategy.strategies.append(AdjustWeightStrategy())
