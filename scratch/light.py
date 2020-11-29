import time

import typer

from gpiozero import Device, MCP3008

# from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()

from gpiozero import MCP3008

light = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)


def main(num: int = 100):
    for i in range(num):
        PRECISION = 5
        vals = []
        for i in range(3):
            try:
                val = light.value
                vals.append(val)
            except OSError:
                val = None
            time.sleep(0.01)
        if vals:
            mean_val = sum(vals) / len(vals)
            mean_val = round(mean_val, PRECISION)
            print(f"val: {mean_val}")
        else:
            print("value not collected")

        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
