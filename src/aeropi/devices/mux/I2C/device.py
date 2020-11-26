import adafruit_tca9548a
import board
import busio
from aeropi.devices.sensor.I2C.air.si7021 import SI7021
from aeropi.devices.sensor.I2C.distance.vl53l0x import VL5310X


class I2CMux:
    def __init__(self, device_tuple, SCL_pin=board.SCL, SDA_pin=board.SDA):
        # NOTE: accepting tuples currently because I'm not sure what the config
        # will look like yet

        # connected = (name, address, channel, device, fn)
        if device_tuple is None:
            raise ValueError("no devices specified in `device_tuple`")

        names = {dt[0] for dt in device_tuple}
        addresses = {dt[1] for dt in device_tuple}
        channels = {dt[2] for dt in device_tuple}
        device_types = {dt[3] for dt in device_tuple}
        device_fns = {dt[4] for dt in device_tuple}

        # "fn": None --> resort to default fn
        ALLOWED_DEVICES = {
            "vl53l0x": {"device_class": VL5310X, "fn": None},
            "si7021": {"device_class": SI7021, "fn": None},
        }
        for dt in device_tuple:
            if len(dt) != 4:
                raise ValueError(
                    f"`device_tuple` entry expected to be length 4, not {len(dt)}: {device_tuple}\n"
                    f"> `device_tuple` should be (name, address, channel, device_type)"
                )

        if not names:
            raise ValueError("no names specified")
        for name in names:
            if not isinstance(name, str):
                raise ValueError(
                    f"name ({name}) is expected to be an {str}, not {type(name)}"
                )

        # If one of the devices is incorrect, do not initialize
        if not channels:
            raise ValueError("no channels specified")
        for c in channels:
            if not isinstance(c, int):
                raise ValueError(
                    f"channel ({c}) is expected to be an int, not {type(c)}"
                )
            if c > 7 or c < 0:
                raise ValueError(f"channel ({c}) expected to be in [0,7]")

        if not addresses:
            raise ValueError(f"no addresses specified")
        for address in addresses:
            if address not in [*range(0x70, 0x77 + 1)]:
                raise ValueError(
                    f"address {address} is invalid. Please select from {[hex(v) for v in [*range(0x70,0x77+1)]]}"
                )

        if not device_types:
            raise ValueError("no device_types specified")
        for device_name in device_types:
            if device_name not in ALLOWED_DEVICES:
                raise ValueError(
                    f"device {device_name} not currently allowed. please select from {ALLOWED_DEVICES.keys()}"
                )

        if not device_fns:
            pass
        else:
            if len(device_fns) != len(device_types):
                raise ValueError(
                    f"device_fns does not match device_types: \nfns:{device_types}, \ndts:{device_types}"
                )

        # Initialize I2C bus and sensor.
        i2c = busio.I2C(SCL_pin, SDA_pin)

        addr_to_tca = {}
        for addr in addresses:
            addr_to_tca[addr] = adafruit_tca9548a.TCA9548A(i2c, address=addr)

        devices = {}
        for name, addr, channel, device_name, dev_fn in device_tuple:
            devices[name] = {}
            # TODO: could allow options here
            cur_dev_class = ALLOWED_DEVICES[device_name]["device_class"]
            cur_tca = addr_to_tca[addr]
            device = cur_dev_class(cur_tca[channel])
            devices[name]["device"] = device
            available_fns = [
                f for f in dir(devices[name]["device"]) if not f.startswith("_")
            ]
            if dev_fn is not None:
                if dev_fn not in available_fns:
                    raise ValueError(
                        f"specified fn ({dev_fn}) for {name} not available for {device}.\n"
                        f"please select from {available_fns}"
                    )
                fn_name = dev_fn
            else:
                fn_name = "return_value"
            try:
                devices[name]["fn"] = devices[name]["device"].__dict__[fn_name]
            except KeyError:
                raise ValueError(
                    f"specified fn ({fn_name}) for {name} not available for {device}.\n"
                    f"please select from {available_fns}"
                )

        self.devices = devices

    def return_value(self, name, **kwargs):
        if name is None:
            return ValueError(
                f"no name specified. please select from {self.devices.keys()}"
            )
        if not isinstance(name, str):
            return ValueError(f"`name` is expected to be type {str}, not {type(name)}")
        try:
            dev_d = self.devices[name]
        except KeyError:
            raise ValueError(
                f"{name} is not available. please select from {self.devices.keys()}"
            )
        value = dev_d["fn"](**kwargs)
        return value
