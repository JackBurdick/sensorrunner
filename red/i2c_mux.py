import board
import busio
import adafruit_tca9548a
import adafruit_vl53l0x


class TofMux:
    def __init__(
        self,
        channels,
        SCL_pin=board.SCL,
        SDA_pin=board.SDA,
    ):
        self.MM_TO_INCH = 0.0393701

        if not isinstance(channels, list):
            raise ValueError(
                f"channels expected to be list of ints, not {type(channels)}"
            )
        for c in channels:
            if not isinstance(c, int):
                raise ValueError(
                    f"channel ({c}) is expected to be an int, not {type(c)}"
                )
            if c > 7 or c < 0:
                raise ValueError(f"channel ({c}) expected to be in [0,7]")

        self.connect_inds = channels

        # Initialize I2C bus and sensor.
        i2c = busio.I2C(SCL_pin, SDA_pin)

        # mux
        tca = adafruit_tca9548a.TCA9548A(i2c)

        # each sensor
        sensors = {}
        for c in channels:
            # TODO: TimeoutError: [Errno 110] Connection timed out
            tmp_sensor = adafruit_vl53l0x.VL53L0X(tca[c])
            tmp_sensor.measurement_timing_budget = 200000
            sensors[c] = tmp_sensor
        self.sensors = sensors

    def obtain_reading(self, c_num, precision=3, unit="in"):
        if not isinstance(c_num, int):
            raise ValueError(
                f"c_num ({c_num}) expected to be an int, not ({type(c_num)}"
            )
        if c_num not in self.sensors.keys():
            raise ValueError(
                f"requested channel num {c_num} not available. select from {list(self.sensors.keys())}"
            )

        try:
            tmp_range = self.sensors[c_num].range
        except OSError:
            tmp_range = None

        # TODO: keep track of these in dict
        if tmp_range is not None:
            if unit == "in":
                tmp_range *= self.MM_TO_INCH
            else:
                raise ValueError(f"unit {unit} not currently supported")

        out = round(tmp_range, precision)
        return out