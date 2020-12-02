import psutil
import re, uuid
import datetime


class CurrentDevice:
    def __init__(self, name):
        if name is None:
            raise ValueError(f"name should be initialized")
        if not isinstance(name, str):
            raise ValueError(
                f"name ({name}) is expected to be type {str}, not {type(name)}"
            )
        self.name = name

    def return_value(self):
        # TODO: wrap in try + include defaults
        device_dict = {}

        device_dict["name"] = self.name

        _disk = psutil.disk_usage("/")
        # int
        disk_total = _disk.total
        device_dict["disk_total"] = disk_total
        # int
        disk_used = _disk.used
        device_dict["disk_used"] = disk_used

        # memory
        _mem = psutil.virtual_memory()
        # int
        mem_total = _mem.total
        device_dict["mem_total"] = mem_total
        # int
        mem_used = _mem.used
        device_dict["mem_used"] = mem_used

        # load
        # float
        load_min_avg = psutil.getloadavg()[0]
        device_dict["load_min_avg"] = load_min_avg

        # temp
        # float
        cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0].current
        device_dict["cpu_temp"] = cpu_temp

        # processes
        # int
        num_pids = len(psutil.pids())
        device_dict["num_pids"] = num_pids
        # network
        # bool
        wifi_isup = psutil.net_if_stats()["wlan0"].isup
        device_dict["wifi_isup"] = wifi_isup

        # time
        _cur_time = datetime.datetime.now()
        _boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        # int
        run_time = (_cur_time - _boot_time).seconds
        device_dict["run_time"] = run_time

        # identifier
        # int
        uuid_ident = uuid.getnode()
        device_dict["uuid_ident"] = uuid_ident
        # str
        mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        device_dict["mac"] = mac

        return device_dict

    @staticmethod
    def build_task_params(device_name, device_dict):
        """
        """
        DEFAULT_FN_NAME = "return_value"

        entry_specs = {}
        for comp_name, comp_dict in device_dict.items():
            dev_dict = comp_dict.copy()
            entry_d = {}
            fn_name = comp_dict["fn_name"]
            if fn_name is None:
                fn_name = DEFAULT_FN_NAME
            entry_d["name"] = f"{device_name}_{comp_name}_{fn_name}"
            # TODO: make more robust
            entry_d["task"] = "aeropi.tasks.devices.DEVICE.tasks.CurrentDevice_run"
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
