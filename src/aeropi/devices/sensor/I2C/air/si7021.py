import adafruit_si7021


class SI7021:
    def __init__(self, channel, precision=3, unit="in"):
        device = adafruit_si7021.SI7021(channel)
        self.device = device
        self.precision = precision
        self.unit = unit
        self.MM_TO_INCH = 0.0393701

    def return_value(self, precision=3, unit="f"):

        try:
            tmp_temp = self.device.temperature
        except OSError:
            tmp_temp = None
        if unit == "f":
            tmp_temp = tmp_temp * 1.8 + 32
        elif unit == "c":
            pass
        else:
            raise ValueError(f"unit {unit} not recognized. please select `f` or `c`")

        try:
            tmp_rh = self.device.relative_humidity
        except OSError:
            tmp_rh = None
        return (tmp_temp, tmp_rh)
