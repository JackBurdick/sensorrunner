from aeropi.tasks.i2c.I2CMux import I2CMux

# (name, address, channel, device)
dev_tuple = [
    ("env_a", 0x72, 2, "si7021"),
    ("dist_a", 0x70, 0, "vl53l0x"),
    ("dist_b", 0x70, 1, "vl53l0x"),
    ("dist_c", 0x72, 0, "vl53l0x"),
    ("dist_d", 0x72, 1, "vl53l0x"),
]

my_mux = I2CMux(dev_tuple)

for dt in dev_tuple:
    v = my_mux.return_value(dt[0])
    print(f"{dt[0]}: {v}")