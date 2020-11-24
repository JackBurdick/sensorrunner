from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder as KPH
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.element.bool import Bool
# from crummycm.validation.types.values.compound.multi import Multi

I2C_DEVICES = ["vl53l0x", "si7021"]


TEMPLATE = {
    # TODO: include task information
    KPH("I2C", exact=True): {
        KPH("name", multi=True): {
            "channel": Numeric(required=True, to_lower=True),
            "address": Numeric(required=True, to_lower=True),
            "device": Text(required=True, is_in_list=I2C_DEVICES),
        }
    }
}
