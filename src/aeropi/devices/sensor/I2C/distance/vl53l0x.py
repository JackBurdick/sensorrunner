import adafruit_vl53l0x


class VL5310X:
    def __init__(self, channel, precision=3, unit="in"):
        device = adafruit_vl53l0x.VL53L0X(channel)
        self.device = device
        self.precision = precision
        if unit:
            if not isinstance(unit, str):
                raise ValueError(
                    f"unit ({unit}) is expected to be type {str}, not {type(unit)}"
                )
            if unit not in ["mm", "in"]:
                raise ValueError(f"unit {self.unit} not currently supported")
        self.unit = unit
        self.MM_TO_INCH = 0.0393701

    def return_value(self):
        try:
            tmp_range = self.device.range
        except OSError:
            tmp_range = None

        # TODO: keep track of these in dict
        if tmp_range is not None:
            if self.unit == "in":
                tmp_range *= self.MM_TO_INCH

            out = round(tmp_range, self.precision)
        else:
            out = tmp_range

        return out
