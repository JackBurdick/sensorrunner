import crummycm as ccm
from aeropi.config.template import TEMPLATE as DEFAULT_TEMPLATE
from aeropi.devices.demux.gpio.device import GPIODemux
from aeropi.devices.mux.I2C.device import I2CMux

# TODO: Mapper, config key to class


def build_devices_from_config(config):

    """
    TODO:
      1) create dict that is {"name": Device}
      2) check config keys against a dict of all classes in `devices` 
      3) have config mirror init params of Devices such that Device(**params)
    """
    DEVICES = {}

    try:
        i2cmux_config = config["I2CMux"]
    except KeyError:
        i2cmux_config = None
    if i2cmux_config:
        i2c_dev = I2CMux(i2cmux_config)
        DEVICES["I2CMux"] = i2c_dev

    try:
        GPIODemux_config = config["GPIODemux"]
    except KeyError:
        GPIODemux_config = None
    if GPIODemux_config:
        for gpiod_name, gpio_d in GPIODemux_config.items():
            gpio_dev = GPIODemux(gpiod_name, gpio_d["init"], gpio_d["devices"])
            # TODO: fix
            # DEVICES["GPIODemux"][gpiod_name] = gpio_dev
        DEVICES["GPIODemux"] = gpio_dev

    return DEVICES


def build_task_params_from_config(config):

    """
    TODO: standardize getattr(DEV, 'build_tasks')

    NOTE: rather than be a seperate call, this logic will likely happen at the
    same time as building the devices. HOwever, right now they are separate

    """
    task_params = {}
    for device_type, device_dict in config.items():
        if device_type == "I2CMux":
            cur_dev_name = device_type
            task_params[device_type] = {}
            cur_tasks = I2CMux.build_task_params(device_type, config["I2CMux"])
            task_params[device_type][cur_dev_name] = cur_tasks
        elif device_type == "GPIODemux":
            task_params[device_type] = {}
            for cur_dev_name, cur_config in config["GPIODemux"].items():
                task_params[device_type][cur_dev_name] = {}
                cur_tasks = GPIODemux.build_task_params(
                    cur_dev_name, cur_config["devices"]
                )
                task_params[device_type][cur_dev_name] = cur_tasks
        else:
            raise ValueError(f"device type {device_type} unsupported")

    return task_params


# {
#     "I2CMux": {
#         "env_a": {
#             "channel": 2,
#             "address": 114,
#             "device_type": "si7021",
#             "params": {"run": {"unit": "f"}, "schedule": {"frequency": 1800.0}},
#             "fn_name": None,
#         },
#         "dist_a": {
#             "channel": 0,
#             "address": 112,
#             "device_type": "vl53l0x",
#             "params": {"run": {"unit": "in"}, "schedule": {"frequency": 1800.0}},
#             "fn_name": None,
#         },
#         "dist_b": {
#             "channel": 1,
#             "address": 112,
#             "device_type": "vl53l0x",
#             "params": {"run": {"unit": "in"}, "schedule": {"frequency": 1800.0}},
#             "fn_name": None,
#         },
#         "dist_c": {
#             "channel": 0,
#             "address": 114,
#             "device_type": "vl53l0x",
#             "params": {"run": {"unit": "in"}, "schedule": {"frequency": 1800.0}},
#             "fn_name": None,
#         },
#         "dist_d": {
#             "channel": 1,
#             "address": 114,
#             "device_type": "vl53l0x",
#             "params": {"run": {"unit": "in"}, "schedule": {"frequency": 1800.0}},
#             "fn_name": None,
#         },
#     },
#     "GPIODemux": {
#         "demux_a": {
#             "init": {"gpio_pins_ordered": [25, 23, 24, 17], "pwr_pin": 27},
#             "devices": {
#                 "a": {
#                     "index": 0,
#                     "device_type": "switch_low",
#                     "params": {
#                         "run": {"on_duration": 1.7, "unit": "seconds"},
#                         "schedule": {"frequency": 4.0},
#                     },
#                 },
#                 "b": {
#                     "index": 1,
#                     "device_type": "switch_low",
#                     "params": {
#                         "run": {"on_duration": 1.3, "unit": "seconds"},
#                         "schedule": {"frequency": 3.0},
#                     },
#                 },
#             },
#         }
#     },
# }
