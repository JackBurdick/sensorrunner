import redis
from aeropi.secrets import REDIS_GLOBAL_host, REDIS_GLOBAL_port, REDIS_GLOBAL_db

r = redis.Redis(host=REDIS_GLOBAL_host, port=REDIS_GLOBAL_port, db=REDIS_GLOBAL_db)

USER_CONFIG = r.get("USER_CONFIG_LOCATION")