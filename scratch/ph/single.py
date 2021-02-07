from atlas_i2c import AtlasI2C


sensor_address = 99
dev = AtlasI2C()
dev.set_i2c_address(sensor_address)


for i in range(10):
    res = dev.query("R", processing_delay=1500)
    print(res)
    print(res.status_code)
    print(res.data)
    time.sleep(2)