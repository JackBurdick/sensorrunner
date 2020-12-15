import adafruit_vl53l0x


class VL5310X:
    def __init__(self, channel, tca=None, precision=3):
        if tca:
            channel = tca[channel]
        device = adafruit_vl53l0x.VL53L0X(channel)
        self.device = device
        self.precision = precision
        self.accepted_units = ["mm", "in"]
        self.MM_TO_INCH = 0.0393701

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
                    f"unit {unit} not currently supported. Please select from {self.accepted_units}"
                )
        else:
            raise ValueError(f"`unit` is expected to exist")

        try:
            tmp_range = self.device.range
        except OSError:
            tmp_range = None

        if tmp_range is not None:
            if unit == "in":
                tmp_range *= self.MM_TO_INCH
            elif unit == "m":
                pass
            out = round(tmp_range, self.precision)
        else:
            out = tmp_range

        return out
