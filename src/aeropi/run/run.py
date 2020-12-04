from aeropi.devices.demux.gpio.device import GPIODemux
from aeropi.devices.mux.I2C.device import I2CMux
from aeropi.devices.SPI.ADC.device import MDC3800
from aeropi.devices.device.device import CurrentDevice


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

    try:
        MDC3800_config = config["MDC3800"]
    except KeyError:
        MDC3800_config = None
    if MDC3800_config:
        MDC3800_dev = MDC3800("MDC3800", MDC3800_config)
        DEVICES["MDC3800"] = MDC3800_dev

    try:
        CurrentDevice_config = config["CurrentDevice"]
    except KeyError:
        CurrentDevice_config = None
    if CurrentDevice_config:
        CurrentDevice_dev = CurrentDevice("CurrentDevice")
        DEVICES["CurrentDevice"] = CurrentDevice_dev

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
        elif device_type == "MDC3800":
            cur_dev_name = device_type
            task_params[device_type] = {}
            cur_tasks = MDC3800.build_task_params(device_type, config["MDC3800"])
            task_params[device_type][cur_dev_name] = cur_tasks
        elif device_type == "GPIODemux":
            task_params[device_type] = {}
            for cur_dev_name, cur_config in config["GPIODemux"].items():
                task_params[device_type][cur_dev_name] = {}
                cur_tasks = GPIODemux.build_task_params(
                    cur_dev_name, cur_config["devices"]
                )
                task_params[device_type][cur_dev_name] = cur_tasks
        elif device_type == "CurrentDevice":
            cur_dev_name = device_type
            task_params[device_type] = {}
            cur_tasks = CurrentDevice.build_task_params(
                device_type, config["CurrentDevice"]
            )
            task_params[device_type][cur_dev_name] = cur_tasks
        elif device_type == "Event":
            pass
        else:
            raise ValueError(f"device type {device_type} unsupported")

    return task_params
