from atlas_i2c import AtlasI2C
import time
import io
import fcntl

import board
import busio
import smbus

class AtlasResponse:
    name: str
    address: int
    status_code: int
    value: bytes
    
    def __repr__(self):
        return str(self.__class__.__name__) + ": " + f"{self.__dict__}"



# class for the I2C switch 
class TCA9548A(object):
    # init
    def __init__(self,name,address,bus_nr):
        self.name=name
        self.address=address
        self.bus_nr=bus_nr
        self.bus=smbus.SMBus(bus_nr)
       
    def set_channel(self,channel):
        assert channel >= 0 and channel <=7, ValueError(f"channel must be between [0,7], not {channel}")
        self.bus.write_byte(self.address,2**channel)
        time.sleep(0.1)

    def atlas(self, address=0x63):
        self.file_write = io.open(file=f"/dev/i2c-{self.bus_nr}", mode="wb", buffering=0)
        self.file_read = io.open(file=f"/dev/i2c-{self.bus_nr}", mode="rb", buffering=0)

        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, address)
        fcntl.ioctl(self.file_write, I2C_SLAVE, address)


    def read_value(self):
        cmd = "R"
        cmd += "\00"
        self.file_write.write(cmd.encode('latin-1'))
        time.sleep(1.5)
        resp = self.file_read.read(31)
        ar = AtlasResponse()
        ar.status_code = resp[0]
        ar.data = resp[1:].strip().strip(b"\x00")
        print(ar)



ADDR = 0x70
tca = TCA9548A('atlas_mux',ADDR,1)
tca.set_channel(3)
tca.atlas()

tca.read_value()

print("-----"*8)
