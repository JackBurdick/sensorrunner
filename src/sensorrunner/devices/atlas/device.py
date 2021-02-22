import smbus
import time
import fcntl
import io

from sensorrunner.devices.sensor.atlas.ph import PhSensor


class AtlasResponse:
    name: str
    address: int
    status_code: int
    value: bytes

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + f"{self.__dict__}"


class AtlasI2cMux:
    def __init__(
        self,
        init_config,
        # devices
        devices_config,
    ):

        # "fn": None --> resort to default fn
        self.ALLOWED_DEVICES = {
            "pH": {"device_class": PhSensor, "fn": None},
        }
        if init_config is None:
            raise ValueError("no init params specified in `init_config`")
        if devices_config is None:
            raise ValueError("no devices specified in `device_dict`")

        try:
            self.address = init_config["address"]
        except KeyError:
            raise ValueError(f"must specify address in `init_config`\n > {init_config}")
        try:
            bus_num = init_config["bus_num"]
        except KeyError:
            bus_num = 1

        # we're using a tca9548a but not using the standard library for reading+writing
        self.bus = smbus.SMBus(bus_num)

        # init devices
        devices = {}
        for d_name, dd in devices_config["devices"]:
            devices["name"] = d_name
            try:
                cur_c = dd["channel"]
            except KeyError:
                raise ValueError(
                    f"No `channel` is specified for {d_name} from {devices_config}"
                )
            if not cur_c in range(9):
                raise ValueError(f"channel must be a value between [0,8], not {cur_c}")

            try:
                cur_a = dd["address"]
            except KeyError:
                raise ValueError(
                    f"No `address` is specified for {d_name} from {devices_config}"
                )

            try:
                cur_cmd_str = dd["cmd_str"]
            except KeyError:
                raise ValueError(
                    f"No `cmd_str` is specified for {d_name} from {devices_config}"
                )

            try:
                cur_dev_class = self.ALLOWED_DEVICES[dd["device_type"]]["device_class"]
            except KeyError:
                raise ValueError(
                    f"device type {dd['device_type']} is unsupported. Please select from {self.ALLOWED_DEVICES.keys()}"
                )

            try:
                init_params = dd["params"]["init"]
            except KeyError:
                init_params = {}

            cur_device = cur_dev_class(cur_c, cur_a, cur_cmd_str, **init_params)
            devices[d_name]["device_type"] = cur_device

        self.devices = devices

    def set_channel(self, channel):
        assert channel >= 0 and channel <= 7, ValueError(
            f"channel must be between [0,7], not {channel}"
        )
        self.reset_channels()
        self.bus.write_byte(self.address, 2 ** channel)
        time.sleep(0.1)

    def reset_channels(self):
        self.bus.write_byte(self.address, 0)  # all off

    def send_cmd(self, cmd="R", channel=None, address=None, reading_delay_s=1.5):
        self.set_channel(channel)

        _I2C_rep = 0x703
        with io.open(file=f"/dev/i2c-{self.bus_num}", mode="wb", buffering=0) as wfp:
            fcntl.ioctl(wfp, _I2C_rep, address)
            # cmd = "R"
            cmd += "\00"
            wfp.write(cmd.encode("latin-1"))

        time.sleep(reading_delay_s)

        ar = AtlasResponse()
        with io.open(file=f"/dev/i2c-{self.bus_num}", mode="rb", buffering=0) as rfp:
            fcntl.ioctl(rfp, _I2C_rep, address)
            resp = rfp.read(31)
            ar.status_code = resp[0]
            ar.data = resp[1:].strip().strip(b"\x00")

        # set all channels off
        self.reset_channels()

        return ar

    def return_value(self, name, params):
        if name is None:
            return ValueError(
                f"no name specified. please select from {self.devices.keys()}"
            )
        if not isinstance(name, str):
            return ValueError(f"`name` is expected to be type {str}, not {type(name)}")
        try:
            cur_device = self.devices[name]
        except KeyError:
            raise ValueError(
                f"{name} is not available. please select from {self.devices.keys()}"
            )

        # obtain value
        try:
            value = self.send_cmd(
                cmd=cur_device.cmd_str,
                channel=cur_device.channel,
                address=cur_device.address,
            )
        except OSError:
            value = None

        if value and cur_device.precision:
            value = round(value, cur_device.precision)

        return value

    @staticmethod
    def build_task_params(device_name, device_dict):
        DEFAULT_FN_NAME = "return_value"
        entry_specs = {}
        for comp_name, comp_dict in device_dict["devices"].items():
            dev_dict = comp_dict.copy()
            entry_d = {}
            fn_name = comp_dict["fn_name"]
            if fn_name is None:
                fn_name = DEFAULT_FN_NAME
            entry_d["name"] = f"{device_name}_{comp_name}_{fn_name}"
            # TODO: make more robust
            entry_d[
                "task"
            ] = "sensorrunner.tasks.devices.AtlasI2cMux.tasks.AtlasI2cMux_run"
            # maybe make schedule outside this?
            entry_d["run_every"] = comp_dict["params"]["schedule"]["frequency"]
            if not isinstance(dev_dict, dict):
                raise ValueError(
                    f"run params ({dev_dict}) expected to be type {dict}, not {type(dev_dict)}"
                )
            # add component name
            dev_dict["name"] = comp_name
            entry_d["kwargs"] = {"dev_dict": dev_dict}
            entry_specs[comp_name] = entry_d
        return entry_specs
