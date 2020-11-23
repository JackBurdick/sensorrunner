import adafruit_tca9548a
import board
import busio

import adafruit_vl53l0x
import adafruit_si7021


class I2CMux:
    def __init__(self, device_tuple, SCL_pin=board.SCL, SDA_pin=board.SDA):
        # NOTE: accepting tuples currently because I'm not sure what the config
        # will look like yet

        # connected = (name, address, channel, device)
        if device_tuple is None:
            raise ValueError("no devices specified in `device_tuple`")

        names = {dt[0] for dt in device_tuple}
        addresses = {dt[1] for dt in device_tuple}
        channels = {dt[2] for dt in device_tuple}
        device_types = {dt[3] for dt in device_tuple}

        ALLOWED_DEVICES = {
            "vl53l0x": {"device_class": adafruit_vl53l0x.VL53L0X, "fn": self._tof_val},
            "si7021": {"device_class": adafruit_si7021.SI7021, "fn": self._env_val},
        }
        self.allowed_devices = ALLOWED_DEVICES
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

        # Initialize I2C bus and sensor.
        i2c = busio.I2C(SCL_pin, SDA_pin)

        addr_to_tca = {}
        for addr in addresses:
            addr_to_tca[addr] = adafruit_tca9548a.TCA9548A(i2c, address=addr)

        devices = {}
        for name, addr, channel, device_name in device_tuple:
            devices[name] = {}
            # TODO: could allow options here
            cur_dev_class = ALLOWED_DEVICES[device_name]["device_class"]
            cur_tca = addr_to_tca[addr]
            device = cur_dev_class(cur_tca[channel])
            devices[name]["device"] = device
            devices[name]["fn"] = ALLOWED_DEVICES[device_name]["fn"]

        self.devices = devices

    def _tof_val(device, precision=3, unit="in"):
        MM_TO_INCH = 0.0393701
        try:
            tmp_range = device.range
        except OSError:
            tmp_range = None

        # TODO: keep track of these in dict
        if tmp_range is not None:
            if unit == "in":
                tmp_range *= MM_TO_INCH
            else:
                raise ValueError(f"unit {unit} not currently supported")
            out = round(tmp_range, precision)
        else:
            out = tmp_range

        return out

    def _env_val(
        device,
    ):
        try:
            tmp_temp = device.temperature * 1.8 + 32
        except OSError:
            tmp_temp = None
        try:
            tmp_rh = device.relative_humidity
        except OSError:
            tmp_rh = None
        return (tmp_temp, tmp_rh)

    def return_value(name, **kwargs):
        if name is None:
            return ValueError(
                f"no name specified. please select from {self.devices.keys()}"
            )
        if not isinstance(name, str):
            return ValueError(f"`name` is expected to be type {str}, not {type(name)}")
        try:
            dev_d = devices[name]
        except KeyError:
            raise ValueError(
                f"{name} is not available. please select from {self.devices.keys()}"
            )
        value = dev_d["fn"](dev_d["device"], **kwargs)
        return value