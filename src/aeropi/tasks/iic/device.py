import board

from .iic_mux import TofMux


def return_tof():
    # tof
    SCL_pin = board.SCL
    SDA_pin = board.SDA
    I2C_CHANNELS = [0, 1]
    dists = TofMux(channels=I2C_CHANNELS, SCL_pin=SCL_pin, SDA_pin=SDA_pin)
    return dists


DISTS = return_tof()