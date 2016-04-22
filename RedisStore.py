import redis


class RedisStore:

    def __init__(self, url, port, db):
        """ database connection """
        try:
            self.redis_pool = redis.ConnectionPool(host=url, port=port, db=db)
        except redis.ConnectionError:
            print("Error: Failed to connect server")
            exit(1)

    def fetch(self, key):
        """ fetch content from database with "key" """
        server = redis.Redis(connection_pool=self.redis_pool)
        return server.get(key)

    def store(self, key, value):
        """ check if "key" exists.
        If true, then do nothing and return "False".
        Else, store {key,value} to database and return "True" """
        server = redis.Redis(connection_pool=self.redis_pool)
        if server.exists(key):
            print("Key %s already exist!", key)
            return False
        else:
            server.set(key, value)
            return True

    def change(self, key, value):
        """ check if "key" exists.
        If true, then change "key" with "value".
        Else, do nothing and return "False". """
        server = redis.Redis(connection_pool=self.redis_pool)
        if server.exists(key):
            server.set(key, value)
            return True
        else:
            print("Key %s not exist!", key)
            return False

    def reset(self):
        """ reset the whole database """
        server = redis.Redis(connection_pool=self.redis_pool)
        server.flushdb()


