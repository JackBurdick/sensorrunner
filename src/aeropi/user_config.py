import redis
import crummycm as ccm
from aeropi.config.template import TEMPLATE
from aeropi.secrets import REDIS_GLOBAL_host, REDIS_GLOBAL_port, REDIS_GLOBAL_db

r = redis.Redis(host=REDIS_GLOBAL_host, port=REDIS_GLOBAL_port, db=REDIS_GLOBAL_db)

config_location = r.get("USER_CONFIG_LOCATION").decode('utf-8')
USER_CONFIG = ccm.generate(config_location, TEMPLATE)
