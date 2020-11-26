import adafruit_si7021


class SI7021:
    def __init__(self, channel, precision=3, unit="in"):
        device = adafruit_si7021.SI7021(channel)
        self.device = device
        self.precision = precision
        self.unit = unit
        self.MM_TO_INCH = 0.0393701

    def return_value(self, precision=3, unit="in"):
        try:
            tmp_temp = self.device.temperature * 1.8 + 32
        except OSError:
            tmp_temp = None
        try:
            tmp_rh = self.device.relative_humidity
        except OSError:
            tmp_rh = None
        return (tmp_temp, tmp_rh)
