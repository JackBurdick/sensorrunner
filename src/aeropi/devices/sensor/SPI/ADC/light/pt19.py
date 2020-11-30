class PT19:
    def __init__(self, device, precision=3):
        self.device = device
        self.precision = precision
        self.accepted_units = ["%"]

    def return_value(self, params):
        try:
            unit = params["unit"]
        except KeyError:
            raise ValueError(f"unit not in {params}")
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

        tmp_val = self.device.value
        if tmp_val is not None:
            out = round(tmp_val, self.precision)
        else:
            out = tmp_val

        return out
