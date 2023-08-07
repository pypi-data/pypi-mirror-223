# Django Redis Session Store

Django Redis Session is a Django session backend that uses Redis as its session store. This package allows multiple Django applications to share user sessions by using the same Redis database as a common session store.

## Installation

You can install Django Redis Session with pip:

```bash
pip install django_redis_session_store
```
## Configuration
To use Django Redis Session, you need to configure several settings in your Django project's settings.py file:

```python

SESSION_ENGINE = 'django_redis_session_store.session_store'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = 'password'
SESSION_REDIS_USER = 'user'
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1800
SESSION_REDIS_TLS = False
```
Please replace the above settings with the actual configuration details of your Redis server.

## Usage
Once Django Redis Session is installed and configured, you can use Django sessions as you would normally. The session data is stored in Redis and can be shared between multiple Django applications.

## Use Case
Imagine that you have two Django applications, App1 and App2, both of which require user authentication. When a user logs into App1, a new session is created and stored in the Redis server. Later, the same user tries to access App2. Since App2 uses the same Redis server for session storage, it recognizes the user's session and does not require the user to log in again.

This shared session feature is particularly useful in microservices architectures, where you might have multiple services that each require user authentication.

## License
This project is licensed under the MIT license. For more details, see the LICENSE file.