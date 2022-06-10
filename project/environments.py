from os import getenv

REDIS_HOST = getenv("REDIS_HOST","127.0.0.1")
REDIS_PORT = getenv("REDIS_PORT","6379")

REDIS_DEFAULT = "0"
REDIS_TOKENS = "1"