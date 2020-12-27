import machine


def setup_sd():
    microsd_config = {
        "miso": 2,
        "mosi": 15,
        "ss": 13,
        "sck": 14,
    }

    sd = machine.SDCard(
        slot=3,
        width=1,
        sck=machine.Pin(microsd_config["sck"]),
        mosi=machine.Pin(microsd_config["mosi"]),
        miso=machine.Pin(microsd_config["miso"]),
        cs=machine.Pin(microsd_config["ss"]),
    )

    return sd


if __name__ == "__main__":
    pass