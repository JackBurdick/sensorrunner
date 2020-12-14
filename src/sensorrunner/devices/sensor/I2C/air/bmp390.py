import adafruit_bmp3xx


class BMP390:
    def __init__(self, channel, precision=3):
        device = adafruit_bmp3xx.BMP3XX_I2C(channel)
        device.pressure_oversampling = 8
        device.temperature_oversampling = 2
        self.device = device
        self.precision = precision
        # TODO: need to support multiple units
        self.accepted_units = ["f", "c", "hPa"]

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

        # pressure
        try:
            tmp_press = self.device.pressure
        except OSError:
            tmp_press = None
        if tmp_press:
            tmp_press = round(tmp_press, self.precision)

        return (tmp_temp, tmp_press)
