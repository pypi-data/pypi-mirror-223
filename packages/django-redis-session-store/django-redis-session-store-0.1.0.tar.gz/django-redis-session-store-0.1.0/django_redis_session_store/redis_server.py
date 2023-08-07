import logging
import redis
from django.conf import settings


class RedisServer:
    __redis = {}

    def __init__(self, session_key):
        self.session_key = session_key
        self.logger = logging.getLogger(__name__)

    def get(self):
        try:
            self.__redis = redis.StrictRedis(
                host=settings.SESSION_REDIS_HOST,
                port=settings.SESSION_REDIS_PORT,
                socket_timeout=settings.SESSION_REDIS_SOCKET_TIMEOUT,
                ssl=settings.SESSION_REDIS_TLS,
                db=settings.SESSION_REDIS_DB,
                username=settings.SESSION_REDIS_USER,
                password=settings.SESSION_REDIS_PASSWORD,
            )

            return self.__redis
        except redis.ConnectionError as e:
            self.logger.error(f"Could not connect to Redis: {str(e)}")
            return None
