import adafruit_tca9548a
import board
import busio


class I2CMux:
    def __init__(self, device_tuples, SCL_pin=board.SCL, SDA_pin=board.SDA):
        # connected = (address, channel, device)
        if device_tuples is None:
            raise ValueError("no devices specified in `device_tuples`")
        addresses = {dt[0] for dt in device_tuples}
        channels = {dt[1] for dt in device_tuples}
        devices = {dt[2] for dt in device_tuples}

        ALLOWED_DEVICES = ["vl53l0x", "si7021"]

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

        if not devices:
            raise ValueError("no devices specified")
        for device in devices:
            if device not in ALLOWED_DEVICES:
                raise ValueError(
                    f"device {device} not currently allowed. please select from {ALLOWED_DEVICES}"
                )

        # Initialize I2C bus and sensor.
        i2c = busio.I2C(SCL_pin, SDA_pin)

        addr_to_tca = {}
        for addr in addresses:
            addr_to_tca[addr] = adafruit_tca9548a.TCA9548A(i2c, address=addr)

    #     # mux
    #     tca = adafruit_tca9548a.TCA9548A(i2c, address=self.address)

    #     # each sensor
    #     sensors = {}
    #     for c in channels:
    #         # TODO: TimeoutError: [Errno 110] Connection timed out
    #         tmp_sensor = adafruit_vl53l0x.VL53L0X(tca[c])
    #         tmp_sensor.measurement_timing_budget = 200000
    #         sensors[c] = tmp_sensor
    #     self.sensors = sensors

    # def obtain_reading(self, c_num, precision=3, unit="in"):
    #     if not isinstance(c_num, int):
    #         raise ValueError(
    #             f"c_num ({c_num}) expected to be an int, not ({type(c_num)}"
    #         )
    #     if c_num not in self.sensors.keys():
    #         raise ValueError(
    #             f"requested channel num {c_num} not available. select from {list(self.sensors.keys())}"
    #         )

    #     try:
    #         tmp_range = self.sensors[c_num].range
    #     except OSError:
    #         tmp_range = None

    #     # TODO: keep track of these in dict
    #     if tmp_range is not None:
    #         if unit == "in":
    #             tmp_range *= self.MM_TO_INCH
    #         else:
    #             raise ValueError(f"unit {unit} not currently supported")

    #     out = round(tmp_range, precision)
    #     return out
