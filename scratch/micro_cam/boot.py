import network
import time
import secrets as sc

import esp

esp.osdebug(None)

import gc

gc.collect()


def network_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(sc.SSID, sc.PASSWORD)
    time.sleep(0.5)
    while station.isconnected() == False:
        time.sleep(0.5)
    ip = station.ifconfig()[0]
    return ip


ip = network_connect()
print(ip)
