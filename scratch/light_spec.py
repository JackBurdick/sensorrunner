import time

import typer

from adafruit_as726x import AS726x_I2C
import adafruit_tca9548a
import board
import busio

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)


# spectral triad
ls = AS726x_I2C(tca2[6])
ls.conversion_mode = ls.MODE_2

# maximum value for ls reading
max_val = 16000

# max number of characters in each graph
max_graph = 80


def graph_map(x):
    return min(int(x * max_graph / max_val), max_graph)


def main(num: int = 100):
    for i in range(num):
        while not ls.data_ready:
            time.sleep(0.1)

        # plot plot the data
        print("\n")
        print(f"V:{ls.violet}")
        print(f"B:{ls.blue}")
        print(f"G:{ls.green}")
        print(f"Y:{ls.yellow}")
        print(f"O:{ls.orange}")
        print(f"R:{ls.red}")

        time.sleep(1)


if __name__ == "__main__":
    typer.run(main)
