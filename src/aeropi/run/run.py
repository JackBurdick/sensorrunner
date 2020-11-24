import crummycm as ccm
from aeropi.config.template import TEMPLATE as DEFAULT_TEMPLATE


def start_tasks_from_config(config_path: str, template=DEFAULT_TEMPLATE):
    config = ccm.generate(config_path, template=template)
    print(config)
    raise NotImplementedError(
        f"`start_tasks_from_config` not yet capable of starting tasks"
    )


# {
#     "I2C": {
#         "env_a": {"channel": 2, "address": 114, "device": "si7021"},
#         "dist_a": {"channel": 0, "address": 112, "device": "vl53l0x"},
#         "dist_b": {"channel": 1, "address": 112, "device": "vl53l0x"},
#         "dist_c": {"channel": 0, "address": 114, "device": "vl53l0x"},
#         "dist_d": {"channel": 1, "address": 114, "device": "vl53l0x"},
#     }
# }

