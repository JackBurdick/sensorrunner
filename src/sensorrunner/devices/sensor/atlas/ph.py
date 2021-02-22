class PhSensor:
    def __init__(self, channel, address=0x63, val_cmd_str="R", precision=3):
        self.channel = channel
        self.address = address
        self.cmd_str = val_cmd_str
        self.precision = precision
