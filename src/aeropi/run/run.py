import crummycm as ccm
from aeropi.config.template import TEMPLATE as DEFAULT_TEMPLATE
from aeropi.devices.mux.I2C.device import I2CMux


def start_tasks_from_config(config_path: str, template=DEFAULT_TEMPLATE):
    config = ccm.generate(config_path, template=template)

    try:
        i2c_confg = config["I2C"]
    except KeyError:
        i2c_confg = None

    i2c_dev = I2CMux(i2c_confg)
    print(i2c_dev)

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
#     },
#     "demux": {
#         "demux_a": {
#             "init": {
#                 "gpio_pins_ordered": [25, 23, 24, 17],
#                 "pwr_pin": 27,
#                 "on_duration": 3.3,
#             },
#             "devices": {
#                 "a": {"index": 0, "on_duration": 1.7},
#                 "b": {"index": 1, "on_duration": 1.3},
#             },
#         }
#     },
# }
