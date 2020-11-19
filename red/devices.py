# from demux import Demux
# from gpiozero import Device
# from gpiozero.pins.mock import MockFactory
# from gpiozero.pins.native import NativeFactory

# import board
# from i2c_mux import TofMux

# """
# temporary file. this will eventually be replaced by a config driven setup

# """

# # TODO: use only single pin lib
# Device.pin_factory = NativeFactory()


# def return_demux():
#     INDEX_PINS = [25, 23, 24, 17]
#     PWR_PIN = 27
#     UNCONNECTED = [11, 12, 13, 14, 15]  # TODO: allow for manual off of pins
#     CONNECTED = []
#     ON_DURATION = 0.3

#     demuxer_a = Demux(
#         INDEX_PINS,
#         PWR_PIN,
#         connected=CONNECTED,
#         unconnected=UNCONNECTED,
#         on_duration=ON_DURATION,
#     )
#     return demuxer_a


# def return_tof():
#     # tof
#     SCL_pin = board.SCL
#     SDA_pin = board.SDA
#     I2C_CHANNELS = [0, 1]
#     dists = TofMux(
#         channels=I2C_CHANNELS,
#         SCL_pin=SCL_pin,
#         SDA_pin=SDA_pin,
#     )
#     return dists


# DEMUX = return_demux()
# DISTS = return_tof()