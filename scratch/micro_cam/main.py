import tinyweb
import time
from cam import setup_cam
from sd import setup_sd
import uos
import network
import gc
import json
from ulog import ULog

# import machine


IMG_PATH_TEMPLATE = "sd/{}__{}__{}.jpg"
V1_BASE_PATH = "/api/v1"
BASE_SD_DIR = "/sd"
IMG_API_PATH = "{}/{}".format(V1_BASE_PATH, "retrieve")

logger = ULog("main.py")

# LED = machine.Pin(1, machine.Pin.OUT)
# time.sleep_ms(300)
# logger.info("led set to pin 1")
# LED.off()
# logger.info("led.off")

# TODO: check if connected
sd = setup_sd(logger)
logger.info("sd setup")
uos.mount(sd, "/sd")
logger.info("sd card mounted")

CAM = None
if not CAM:
    CAM = setup_cam(logger)
logger.info("camera setup")

app = tinyweb.webserver()
logger.debug("app webserver created")


def _write_image(cam_info):
    global CAM
    ret = {}
    if cam_info:
        # LED.on()
        # time.sleep_ms(500)
        buf = CAM.capture()
        img_path = IMG_PATH_TEMPLATE.format(
            cam_info["bucket"], cam_info["index"], cam_info["ts"]
        )
        f = open(img_path, "w")
        f.write(buf)
        time.sleep_ms(100)
        f.close()
        # LED.off()
        ret["path"] = img_path
        ret["bucket"] = cam_info["bucket"]
        ret["index"] = cam_info["index"]
        ret["ts"] = cam_info["ts"]
    return ret


def _basic_parse_qs(raw_qs):
    qs_d = {}
    raw_qstrs = raw_qs.decode("utf-8").split("&")
    for qs in raw_qstrs:
        kv = qs.split("=")
        qs_d[kv[0]] = kv[1]
    return qs_d


class Status:
    url = "{}/{}".format(V1_BASE_PATH, "status")

    def get(self, data):
        mem = {
            "mem_alloc": gc.mem_alloc(),
            "mem_free": gc.mem_free(),
            "mem_total": gc.mem_alloc() + gc.mem_free(),
        }
        sta_if = network.WLAN(network.STA_IF)
        ifconfig = sta_if.ifconfig()
        net = {
            "ip": ifconfig[0],
            "netmask": ifconfig[1],
            "gateway": ifconfig[2],
            "dns": ifconfig[3],
        }
        return {"memory": mem, "network": net}, 200


class Capture:
    url = "{}/{}".format(V1_BASE_PATH, "capture")

    def post(self, data):
        img_cap = None
        if data:
            try:
                cam_info = data["cam"]
            except KeyError:
                cam_info = None
            # cams: {index: ___, ts: ___}
            img_cap = _write_image(cam_info)
        resp = {"cam": img_cap}
        return resp, 200


class SDFiles:
    url = "{}/{}".format(V1_BASE_PATH, "sdfiles")

    def get(self, data):
        files = uos.listdir(BASE_SD_DIR)
        # remove dotfiles
        files = [f for f in files if not f.startswith(".")]
        # {"files": ["now_2.jpg", "0_12_26_2020__11_43_10.jpg"]}
        resp = {"files": files}
        return resp, 400

    def delete(self, data):
        # e.g. "now_2.jpg"
        try:
            f_name = data["file_name"]
        except KeyError:
            f_name = None
        if f_name:
            f_path = "{}/{}".format(BASE_SD_DIR, f_name)
            try:
                f = open(f_path, "r")
            except OSError:
                resp = ({"message": "file not found: {}".format(f_path)}, 400)
            else:
                f.close()
                uos.remove("{}".format(f_path))
                resp = ({"message": "file deleted: {}".format(f_path)}, 200)
        else:
            resp = ({"message": "no `file_name` detected. data: {}".format(data)}, 400)
        return resp[0], resp[1]


@app.route(IMG_API_PATH)
async def images(req, resp):
    qs = req.query_string
    try:
        qs_d = _basic_parse_qs(qs)
    except Exception:
        # catch all exceptions
        qs_d = None
    if qs_d:
        try:
            ts = qs_d["ts"]
        except KeyError:
            ts = None
        try:
            index = qs_d["index"]
        except KeyError:
            index = None
        try:
            bucket = qs_d["bucket"]
        except KeyError:
            bucket = None
    else:
        ts = None
        index = None
        bucket = None

    if bucket is not None and index is not None and ts is not None:
        fp = IMG_PATH_TEMPLATE.format(bucket, index, ts)
        await resp.send_file(fp, content_type="image/jpeg")
    else:
        msg = {
            "message": "bucket ({}) index ({}) or ts ({}) missing: qs_d:{}".format(
                bucket, index, ts, qs_d
            )
        }
        resp.code = 400
        resp.add_header("Content-Type", "application/json")
        msg_json = json.dumps(msg)
        resp.add_header("Content-Length", len(msg_json))
        await resp._send_headers()
        await resp.send(msg_json)


logger.debug("add resource: {}".format(IMG_API_PATH))


def run():

    app.add_resource(Status, Status.url)
    logger.debug("add resource: {}".format(Status.url))

    app.add_resource(Capture, Capture.url)
    logger.debug("add resource: {}".format(Capture.url))

    app.add_resource(SDFiles, SDFiles.url)
    logger.debug("add resource: {}".format(SDFiles.url))

    logger.debug("calling app run")
    logger.to_file("/sd/mylog.json")
    app.run(host="0.0.0.0", port=8081)


if __name__ == "__main__":
    logger.debug("running as script")
    run()