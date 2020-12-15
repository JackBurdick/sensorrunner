import adafruit_veml6070


class VEML6070:
    def __init__(self, channel, tca=None, precision=3):
        if tca:
            channel = tca[channel]
        # favor precision
        device = adafruit_veml6070.VEML6070(channel, "VEML6070_4_T")
        self.device = device
        self.precision = precision
        # output is unitless, 'light intensity' - 0-9999
        self.accepted_units = ["intensity"]

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
            tmp_uv = self.device.uv_raw
        except OSError:
            tmp_uv = None

        if tmp_uv is not None:
            out = round(tmp_uv, self.precision)
        else:
            out = tmp_uv

        return out
