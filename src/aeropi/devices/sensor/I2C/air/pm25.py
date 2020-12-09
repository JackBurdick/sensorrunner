from adafruit_pm25.i2c import PM25_I2C
from aeropi.devices.util import average_dict
import time
from gpiozero import Device, DigitalOutputDevice
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()


class PM25:
    def __init__(self, channel, pwr_pin, num_iterations=3, precision=3):
        self.pwr_pin = pwr_pin = DigitalOutputDevice(pwr_pin)
        pwr_pin.on()
        # NOTE: must allow device to be on for initialization
        time.sleep(1)
        try:
            device = PM25_I2C(channel)
        except OSError:
            # Try one more time
            pwr_pin.on()
            time.sleep(1)
            try:
                device = PM25_I2C(channel)
            except Exception:
                raise OSError(
                    f"Unable to initialize PM25 device. please double check {pwr_pin} is correct on/off pin"
                )
        self.device = device
        self.num_iterations = num_iterations
        self.precision = precision
        self.accepted_units = ["ug/m^3", "um/0.1L"]

    def _parse_sensor(self):
        try:
            aqdata = self.device.read()
        except (OSError, RuntimeError) as e:
            print(f"ERROR!: {e}")
            aqdata = None

        vals, units = {}, {}
        if aqdata:
            # keys
            # reading key, unit, new_name
            # Particle Matter concentrations of different size particles in micro-gram per cubic meter
            sensor_keys = [
                ("particles 03um", "03um/0.1L", "03um"),
                ("particles 05um", "05um/0.1L", "05um"),
                ("particles 10um", "10um/0.1L", "10um"),
                ("particles 25um", "25um/0.1L", "25um"),
                ("particles 50um", "50um/0.1L", "50um"),
                ("particles 100um", "100um/0.1L", "100um"),
                ("pm10 standard", "ug/m^3", "standard_pm10"),
                ("pm10 env", "ug/m^3", "pm10"),
                ("pm25 standard", "ug/m^3", "standard_pm25"),
                ("pm25 env", "ug/m^3", "pm25"),
                ("pm100 standard", "ug/m^3", "standard_pm100"),
                ("pm100 env", "ug/m^3", "pm100"),
            ]

            for skt in sensor_keys:
                vals[skt[2]] = aqdata[skt[0]]
                units[skt[2]] = skt[1]
        return vals, units

    def return_value(self, **kwargs):
        # TODO: this is a pretty rough first cut
        # the units will need to be addressed more elegantly
        try:
            unit = kwargs["unit"]
        except KeyError:
            raise ValueError(f"unit not in {kwargs}")
        if unit:
            if not isinstance(unit, str):
                raise ValueError(
                    f"unit ({unit}) is expected to be type {str}, not {type(unit)}"
                )
            if unit not in self.accepted_units:
                raise ValueError(
                    f"unit {unit} not currently supported. Please select from {self.accepted_units}"
                )
        else:
            raise ValueError(f"`unit` is expected to exist")
        # TODO: I'm not doing anything with the units here

        # NOTE: the device needs to run for 30+ seconds to initialize
        self.pwr_pin.on()
        time.sleep(45)

        raw_vals = {}
        cur_u = {}
        for i in range(self.num_iterations):
            cur_v, cur_u = self._parse_sensor()
            # sleep betweek events
            time.sleep(10)
            raw_vals[f"{i}"] = cur_v
        self.pwr_pin.off()
        val_dict = average_dict(raw_vals)

        # format output
        if self.precision:
            for k, v in val_dict:
                val_dict[k] = round(v, self.precision)

        return (val_dict, cur_u)
