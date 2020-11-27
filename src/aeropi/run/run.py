import crummycm as ccm
from aeropi.config.template import TEMPLATE as DEFAULT_TEMPLATE
from aeropi.devices.demux.gpio.device import GPIODemux
from aeropi.devices.mux.I2C.device import I2CMux


def build_devices_from_config(config):

    """
    TODO:
      1) create dict that is {"name": Device}
      2) check config keys against a dict of all classes in `devices` 
      3) have config mirror init params of Devices such that Device(**params)
    """

    try:
        i2cmux_config = config["I2CMux"]
    except KeyError:
        i2cmux_config = None
    i2c_dev = I2CMux(i2cmux_config)
    print(i2c_dev)

    try:
        GPIODemux_config = config["GPIODemux"]
    except KeyError:
        GPIODemux_config = None
    for gpiod_name, gpio_d in GPIODemux_config.items():
        gpio_dev = GPIODemux(gpiod_name, gpio_d["init"], gpio_d["devices"])
        print(gpio_dev)

    raise NotImplementedError(
        f"`build_devices_from_config` not yet capable of starting tasks"
    )


# {
#     "GPIODemux": {
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
#     }
# }

# {
#     "I2C": {
#         "env_a": {"channel": 2, "address": 114, "device": "si7021"},
#         "dist_a": {"channel": 0, "address": 112, "device": "vl53l0x"},
#         "dist_b": {"channel": 1, "address": 112, "device": "vl53l0x"},
#         "dist_c": {"channel": 0, "address": 114, "device": "vl53l0x"},
#         "dist_d": {"channel": 1, "address": 114, "device": "vl53l0x"},
#     },
#
# }
