import adafruit_si7021


class SI7021:
    def __init__(self, channel, precision=3, unit="f"):
        device = adafruit_si7021.SI7021(channel)
        self.device = device
        self.precision = precision
        if unit:
            if not isinstance(unit, str):
                raise ValueError(
                    f"unit ({unit}) is expected to be type {str}, not {type(unit)}"
                )
            if unit not in ["f", "c"]:
                raise ValueError(f"unit {self.unit} not currently supported")
        self.unit = unit
        self.MM_TO_INCH = 0.0393701

    def return_value(self):

        try:
            tmp_temp = self.device.temperature
        except OSError:
            tmp_temp = None
        if self.unit == "f":
            tmp_temp = tmp_temp * 1.8 + 32
        try:
            tmp_rh = self.device.relative_humidity
        except OSError:
            tmp_rh = None
        return (tmp_temp, tmp_rh)
