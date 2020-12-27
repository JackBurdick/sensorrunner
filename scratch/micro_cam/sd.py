import machine


def setup_sd(logger):
    microsd_config = {
        "miso": 2,
        "mosi": 15,
        "ss": 13,
        "sck": 14,
    }
    logger.debug("microsd_config: {}".format(microsd_config))

    sd = machine.SDCard(
        slot=3,
        width=1,
        sck=machine.Pin(microsd_config["sck"]),
        mosi=machine.Pin(microsd_config["mosi"]),
        miso=machine.Pin(microsd_config["miso"]),
        cs=machine.Pin(microsd_config["ss"]),
    )
    logger.debug("sd card initialized: {}".format(sd))

    return sd


if __name__ == "__main__":
    pass