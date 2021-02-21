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


class AtlasMux(object):
    # TCA9548A
    def __init__(self, name, address, bus_num=1):
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

        _I2C_rep = 0x703
        fcntl.ioctl(self.file_read, _I2C_rep, address)
        fcntl.ioctl(self.file_write, _I2C_rep, address)

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

    def read_sensor(self, channel=3, address=0x63, reading_delay_s=1.5):
        self.set_channel(channel)

        _I2C_rep = 0x703
        with io.open(file=f"/dev/i2c-{self.bus_num}", mode="wb", buffering=0) as wfp:
            fcntl.ioctl(wfp, _I2C_rep, address)
            cmd = "R"
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
        self.bus.write_byte(self.address, 0)

        return ar
        #####


MUX_ADDR = 0x70
ph_addr = 0x63
tca = AtlasMux("atlas_mux", MUX_ADDR)
# tca.set_channel(3)
# tca._atlas_setup()
for i in range(10):
    v = tca.read_sensor(channel=3, address=0x63)
    print(f"{i}: {v}")
    print("-----" * 8)
    time.sleep(1)
