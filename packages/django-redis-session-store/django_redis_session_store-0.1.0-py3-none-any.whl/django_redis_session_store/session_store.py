import logging
from typing import Dict, Any

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.core import signing

from django_redis_session_store.redis_server import RedisServer
from django.utils.encoding import force_str as force_unicode


class SessionStore(SessionBase):
    """
    Session Store with Redis Client to share it with Pegasus backend.
    """

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        self.server = RedisServer(session_key).get()

    def load(self) -> Dict[str, str]:
        """
        Load the session data from the server by getting or creating the key and then decodes it.

        Returns:
            Decoded session data or an empty dict.
        """
        session_key = self.get_real_stored_key(self._get_or_create_session_key())

        session_data = self.server.get(session_key)

        if session_data:
            decoded_session_data = self.decode(force_unicode(session_data))
            return decoded_session_data

        self._session_key = None
        return {}

    def encode(self, session_dict: Dict[str, Any]) -> str:
        """
        Encodes the session dict with the key and the salt that we provide.

        Args:
            session_dict: Session key and the data.

        Returns:
            String of the encoded session data.
        """

        return signing.dumps(
            session_dict,
            key=settings.SHARED_SECRET_KEY,
            salt=self.key_salt,
            serializer=self.serializer,
            compress=True,
        )

    def decode(self, encoded_session_data: str) -> Dict[Any, Any]:
        """
        Decodes the session data if there is something wrong with the session data returns nothing and logs it.

        Args:
            encoded_session_data: data that we encoded with our key and salt.

        Returns:
            Decoded data or and empty dictionary.
        """

        try:
            return signing.loads(
                encoded_session_data,
                key=settings.SHARED_SECRET_KEY,
                salt=self.key_salt,
                serializer=self.serializer,
            )
        except signing.BadSignature:
            logger = logging.getLogger("django.security.SuspiciousSession")
            logger.warning("Session data corrupted")
        return {}

    def exists(self, session_key: str) -> int:
        """
        Checks if the session key exist in the server.

        Args:
            session_key:

        Returns:
            0 or 1 but don't know why it is not boolean
        """

        return self.server.exists(self.get_real_stored_key(session_key))

    def create(self) -> None:
        """
        Creates a new unique session key.

        Returns:
            None
        """

        while True:
            self._session_key = self._get_new_session_key()

            try:
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return

    def save(self, must_create=False) -> None:
        """
        Saves the session_key and the data, if there is none it creates one. Save means setting it to the server.
        You need to call this method in if you want to store your session data in Redis. Otherwise, it will be in
        session_cache, and it won't be accessible from shared applications.

        Args:
            must_create: Whether if we want to create new session_key every time.

        Returns:
            None
        """

        if not self.session_key:
            return self.create()
        if must_create and self.exists(self._get_or_create_session_key()):
            raise CreateError
        data = self._get_session(no_load=must_create)
        encoded_data = self.encode(data)

        # setex saves the key and the data to redis with expiry time.
        self.server.setex(
            self.get_real_stored_key(self._get_or_create_session_key()),
            self.get_expiry_age(),
            encoded_data,
        )

    def delete(self, session_key=None) -> None:
        """
        Deletes the key from Redis.

        Args:
            session_key: specific session_key to delete

        Returns:
            None
        """

        if session_key or self.session_key:
            session_key = self.session_key
            self.server.delete(self.get_real_stored_key(session_key))

    @classmethod
    def clear_expired(cls):
        pass

    def get_real_stored_key(self, session_key: str) -> str:
        """
        Returns the real key from the Redis, depending on our prefix.
        Args:
            session_key: session key in string.

        Returns:
            Session key with prefix added if there is one, otherwise just the session key itself.
        """

        prefix = settings.SESSION_REDIS_PREFIX
        if not prefix:
            return session_key
        return ":".join([prefix, session_key])
