import fcntl
import io
import time

import smbus


class AtlasResponse:
    name: str
    address: int
    status_code: int
    value: bytes

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + f"{self.__dict__}"


class TCA9548A(object):
    def __init__(self, name, address, bus_num):
        self.name = name
        self.address = address
        self.bus_num = bus_num
        self.bus = smbus.SMBus(bus_num)

    def set_channel(self, channel):
        assert channel >= 0 and channel <= 7, ValueError(
            f"channel must be between [0,7], not {channel}"
        )
        self.bus.write_byte(self.address, 0)  # all off
        self.bus.write_byte(self.address, 2 ** channel)
        time.sleep(0.1)

    def _atlas_setup(self, address=0x63):
        self.file_write = io.open(
            file=f"/dev/i2c-{self.bus_num}", mode="wb", buffering=0
        )
        self.file_read = io.open(
            file=f"/dev/i2c-{self.bus_num}", mode="rb", buffering=0
        )

        I2C_rep = 0x703
        fcntl.ioctl(self.file_read, I2C_rep, address)
        fcntl.ioctl(self.file_write, I2C_rep, address)

    def read_value(self):
        cmd = "R"
        cmd += "\00"
        self.file_write.write(cmd.encode("latin-1"))
        time.sleep(1.5)
        resp = self.file_read.read(31)
        ar = AtlasResponse()
        ar.status_code = resp[0]
        ar.data = resp[1:].strip().strip(b"\x00")
        return ar


MUX_ADDR = 0x70

tca = TCA9548A("atlas_mux", MUX_ADDR, 1)
tca.set_channel(3)
tca._atlas_setup()

v = tca.read_value()
print(v)
print("-----" * 8)
