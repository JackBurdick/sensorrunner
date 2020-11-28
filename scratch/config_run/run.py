import crummycm as ccm
from aeropi.config.template import TEMPLATE
from aeropi.run.run import build_devices_from_config
from aeropi.secrets import L_CONFIG_DIR, P_CONFIG_DIR

try:
    out = ccm.generate(L_CONFIG_DIR, TEMPLATE)
except FileNotFoundError:
    out = ccm.generate(P_CONFIG_DIR, TEMPLATE)
USER_CONFIG = out

# print("start")
conf = ccm.generate(USER_CONFIG, TEMPLATE)
print(conf)
print("-----" * 8)
devs = build_devices_from_config(conf)
print(devs)
