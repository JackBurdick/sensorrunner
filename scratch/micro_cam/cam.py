import camera


def setup_cam(logger):
    QUALITY = 12
    camera.init(0)
    logger.debug("Camera initialized")
    camera.quality(QUALITY)
    logger.debug("Camera quality set to {}".format(QUALITY))
    return camera


if __name__ == "__main__":
    pass