# -*- encoding: utf8 -*-

identity = lambda x:x


def flatten(xss):
    return [x for xs in xss for x in xs]


def inflatten(xs, map):
    return [xs] if len(map) == 1 else [xs[0:map[0]]] + inflatten(xs[map[0]:], map[1:])


def down(xs):
    return [[x] for x in xs]


def chunks(xs, n, size=None):
    size = int(round(len(xs) / float(n))) if not size else size
    return [xs] if n == 1 else [xs[0:size]] + chunks(xs[size:], n - 1, size)


def first(xs):
    return next(iter(xs), None) if xs else None


def rest(xs):
   it = iter(xs) if xs else None
   return list(it) if it and next(it, None) is not None else None


def assign(x, k, v):
    from copy import deepcopy
    x = deepcopy(x)
    x[k] = v
    return x


def pluck(xs, keys):
    return map(lambda x: reduce(lambda a, k: assign(a, k, x[k]), keys, {}), xs)


def plucks(x, keys):
    return reduce(lambda a, k: assign(a, k, x[k]), keys, {})


def find_index(xs, predicate):
    return reduce(lambda acc, x: acc if acc >= 0 else x[0] if predicate(x[1]) else -1, enumerate(xs), -1)


def extract(xs, key):
    return map(lambda x: x.get(key), xs)


def split(xs, size):
    return [xs[s:s+size] for s in range(0, len(xs), size)]


def partition(xs, predicate):
    return [filter(predicate, xs), filter(lambda x: not predicate(x), xs)]


def uniq(xs):
    return uniq_by(xs, identity)


def uniq_by(xs, iteratee):
    return [] if not xs else uniq_by(rest(xs), iteratee) if iteratee(first(xs)) in map(iteratee, rest(xs)) else [first(xs)] + uniq_by(rest(xs), iteratee)


def sort_by(xs, iteratee, reverse=False):
    return sorted(xs, key=iteratee, reverse=reverse)


def swap(arr, index1, index2):
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp
