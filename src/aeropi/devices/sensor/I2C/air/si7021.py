import adafruit_si7021


class SI7021:
    def __init__(self, channel, precision=3):
        device = adafruit_si7021.SI7021(channel)
        self.device = device
        self.precision = precision
        self.MM_TO_INCH = 0.0393701
        self.accepted_units = ["f", "c"]

    def return_value(self, **kwargs):
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
                    f"unit {self.unit} not currently supported. Please select from {self.accepted_units}"
                )
        else:
            raise ValueError(f"`unit` is expected to exist")

        # temp
        try:
            tmp_temp = self.device.temperature
        except OSError:
            tmp_temp = None
        if tmp_temp is not None:
            if unit == "f":
                tmp_temp = tmp_temp * 1.8 + 32
            elif unit == "c":
                pass
            tmp_temp = round(tmp_temp, self.precision)

        # humidity
        try:
            tmp_rh = self.device.relative_humidity
        except OSError:
            tmp_rh = None
        if tmp_rh:
            tmp_rh = round(tmp_rh, self.precision)

        return (tmp_temp, tmp_rh)
