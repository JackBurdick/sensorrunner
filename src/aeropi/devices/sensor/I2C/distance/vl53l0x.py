import adafruit_vl53l0x


class VL5310X:
    def __init__(self, channel, precision=3, unit="in"):
        device = adafruit_vl53l0x.VL53L0X(channel)
        self.device = device
        self.precision = precision
        self.unit = unit
        self.MM_TO_INCH = 0.0393701

    def return_value(self, precision=3, unit="in"):
        try:
            tmp_range = self.device.range
        except OSError:
            tmp_range = None

        # TODO: keep track of these in dict
        if tmp_range is not None:
            if unit == "in":
                tmp_range *= self.MM_TO_INCH
            else:
                raise ValueError(f"unit {unit} not currently supported")
            out = round(tmp_range, precision)
        else:
            out = tmp_range

        return out
