__author__ = 'zhangchuan'

import random
from redis import Redis

from redis.exceptions import (
    ConnectionError,
    TimeoutError,
)


def out_exec_command(self, connection, command_name, args, options):
    connection.send_command(*args)
    resp = self.parse_response(connection, command_name, **options)
    return resp


class RedisEntity(Redis):
    redis_list = []

    def __init__(self, redis_list):

        super(RedisEntity, self).__init__()
        self.redis_list = redis_list

    def execute_command(self, *args, **options):

        i = random.randint(0, len(self.redis_list) - 1)
        redis_connection = self.redis_list[i]
        pool = self.connection_pool
        command_name = args[0]
        connection = pool.get_connection(command_name, **options)
        try:

            return out_exec_command(redis_connection, connection, command_name, args, options)
        except (ConnectionError, TimeoutError) as e:
            connection.disconnect()
            if not connection.retry_on_timeout and isinstance(e, TimeoutError):
                raise
            return out_exec_command(redis_connection, connection, command_name, args, options)
        finally:
            pool.release(connection)




