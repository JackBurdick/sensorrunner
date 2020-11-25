from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder as KPH
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.compound.multi import Multi
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.element.bool import Bool


I2C_DEVICES = ["vl53l0x", "si7021"]


TEMPLATE = {
    # TODO: include task information
    KPH("I2C", exact=True, required=False): {
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
            "device": Text(required=True, is_in_list=I2C_DEVICES),
        }
    },
    KPH("demux", exact=True, required=False): {
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
                "on_duration": Numeric(required=True, is_type=float, bounds=(0, 5)),
            },
            "devices": {
                KPH("name", multi=True): {
                    "index": Numeric(
                        required=True,
                        is_type=int,
                        bounds=(0, 15),
                        bounds_inclusive=(True, True),
                    ),
                    "on_duration": Numeric(required=True, is_type=float, bounds=(0, 5)),
                }
            },
        }
    },
}
