# -*- coding:utf-8 -*-
from werkzeug.contrib.sessions import SessionStore
import redis
from pickle import dumps , HIGHEST_PROTOCOL, loads

class RedisSessionStore(SessionStore):

    def __init__(self, redisHost, expireTime, redisPort, redisDB, session_class=None):
        SessionStore.__init__(self, session_class)
        self.path = None
        self._redisHost = redisHost
        self._redisPort = redisPort
        self._redisDb = redisDB
        self._expireTime = expireTime
        self._connpool = redis.ConnectionPool(host=self._redisHost, port=self._redisPort, db=redisDB)


    def save(self, session):
        conn = redis.StrictRedis(connection_pool=self._connpool)
        sessionData = dumps(dict(session), HIGHEST_PROTOCOL)
        conn.set(session.sid, sessionData)
        conn.expire(session.sid, self._expireTime)

    def delete(self, session):
        conn = redis.StrictRedis(connection_pool=self._connpool)
        conn.delete(session.sid)

    def get(self, sid):
        if not self.is_valid_key(sid):
            return self.new()
        conn = redis.StrictRedis(connection_pool=self._connpool)
        sessionData = conn.get(sid)
        if sessionData == None:
            return self.new()
        try:
            data = loads(sessionData)
        except Exception:
            data = {}
        return self.session_class(data, sid, False)