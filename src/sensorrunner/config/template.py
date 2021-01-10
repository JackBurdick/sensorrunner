from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder as KPH
from crummycm.validation.types.placeholders.placeholder import ValuePlaceholder as VPH
from crummycm.validation.types.values.compound.multi import Multi
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

from sensorrunner.devices.SPI.ADC.device import MDC3800

# from crummycm.validation.types.values.element.bool import Bool


I2CMux_DEVICES = ["vl53l0x", "si7021", "veml6070", "pm25", "bmp390"]
GPIODemux_DEVICES = ["switch_low"]
MDC3800_DEVICES = ["pt19"]
EVENT_DEVICES = ["vib801s"]
Cams_DEVICES = ["ESPCam"]

TEMPLATE = {
    # TODO: include task information
    KPH("CurrentDevice", exact=True, required=False): {
        KPH("name"): {
            "device_type": Text(required=True, is_in_list=["current_device"]),
            "params": {
                "schedule": {
                    # 0-6hrs
                    "frequency": Numeric(
                        required=False, is_type=float, bounds=(0, 21600)
                    )
                }
            },
            "fn_name": Text(required=False),
        }
    },
    KPH("I2CMux", exact=True, required=False): {
        KPH("name", multi=True): {
            "channel": Numeric(
                required=True, is_type=int, bounds=(0, 7), bounds_inclusive=(True, True)
            ),
            "address": Numeric(
                required=True,
                is_type=int,
                bounds=(0x70, 0x77),
                bounds_inclusive=(True, True),
            ),
            "device_type": Text(required=True, is_in_list=I2CMux_DEVICES),
            "params": {
                KPH("init", required=False, exact=True): {
                    KPH("pwr_pin", required=False, exact=True): Numeric(
                        required=True,
                        is_type=int,
                        bounds=(0, 27),
                        bounds_inclusive=(True, True),
                    ),
                    KPH("init_param_name", multi=True, required=False): VPH(
                        "init_param_value"
                    ),
                },
                "run": {
                    KPH("run_param_name", multi=True, required=False): VPH(
                        "run_param_value"
                    ),
                    "unit": Text(required=True),
                },
                "schedule": {
                    "frequency": Numeric(
                        required=False, is_type=float, bounds=(0, 86400)
                    )
                },
            },
            "fn_name": Text(required=False),
        }
    },
    KPH("Event", exact=True, required=False): {
        KPH("name", multi=True): {
            "device_type": Text(required=True, is_in_list=EVENT_DEVICES),
            "params": {
                "init": {
                    "pin": Numeric(
                        required=True,
                        is_type=int,
                        bounds=(0, 27),
                        bounds_inclusive=(True, True),
                    ),
                    KPH("init_param_name", multi=True, required=False): VPH(
                        "init_param_value"
                    ),
                },
                "events": {
                    "when_activated": Text(required=False),
                    "when_deactivated": Text(required=False),
                },
            },
        }
    },
    KPH("MDC3800", exact=True, required=False): {
        KPH("name", multi=True): {
            "channel": Numeric(
                required=True, is_type=int, bounds=(0, 7), bounds_inclusive=(True, True)
            ),
            "device_type": Text(required=True, is_in_list=MDC3800_DEVICES),
            "params": {
                "run": {
                    KPH("run_param_name", multi=True, required=False): VPH(
                        "run_param_value"
                    ),
                    "unit": Text(required=True),
                },
                "schedule": {
                    "frequency": Numeric(
                        required=False, is_type=float, bounds=(0, 86400)
                    )
                },
            },
            "fn_name": Text(required=False),
        }
    },
    KPH("Cams", exact=True, required=False): {
        # call>bucket, index, ts, local_dir
        KPH("name", multi=True): {
            "device_type": Text(required=True, is_in_list=Cams_DEVICES),
            "params": {
                KPH("init", required=True, exact=True): {
                    "ip_addr": Text(required=True),
                },
                "run": {
                    "bucket": Numeric(is_type=int),
                    "index": Numeric(is_type=int),
                    "local_dir": Text(required=True),
                },
                "schedule": {
                    "schedule": {
                        KPH("schedule_param_name", multi=True, required=False): VPH(
                            "schedule_param_value"
                        )
                    },
                },
            },
            "fn_name": Text(required=False),
        }
    },
    KPH("GPIODemux", exact=True, required=False): {
        KPH("demux_name", required=True, multi=True): {
            "init": {
                "gpio_pins_ordered": Multi(
                    element_types=Numeric(
                        required=True,
                        is_type=int,
                        bounds=(0, 27),
                        bounds_inclusive=(True, True),
                    ),
                    required=True,
                    homogeneous=True,
                ),
                "pwr_pin": Numeric(
                    required=True,
                    is_type=int,
                    bounds=(0, 27),
                    bounds_inclusive=(True, True),
                ),
            },
            "devices": {
                KPH("name", multi=True): {
                    "index": Numeric(
                        required=True,
                        is_type=int,
                        bounds=(0, 15),
                        bounds_inclusive=(True, True),
                    ),
                    "device_type": Text(required=True, is_in_list=GPIODemux_DEVICES),
                    "params": {
                        "run": {
                            "on_duration": Numeric(
                                required=True, is_type=float, bounds=(0, 5)
                            ),
                            "unit": Text(required=True),
                        },
                        "schedule": {
                            "frequency": Numeric(
                                required=False, is_type=float, bounds=(1, 86400)
                            )
                        },
                    },
                    "fn_name": Text(required=False),
                }
            },
        }
    },
}
