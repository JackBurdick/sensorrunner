import tinyweb
import time
from cam import setup_cam
from sd import setup_sd
import uos
import network
import gc
import json
from ulog import ULog

IMG_PATH_TEMPLATE = "sd/{}__{}.jpg"

logger = ULog("main.py")

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


def _write_image(cams):
    global CAM
    ret = {}
    if cams:
        for _, cam_info in cams.items():
            buf = CAM.capture()
            img_path = IMG_PATH_TEMPLATE.format(cam_info["index"], cam_info["ts"])
            f = open(img_path, "w")
            f.write(buf)
            time.sleep_ms(100)
            f.close()
            ret["path"] = img_path
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
    def post(self, data):
        img_cap = None
        if data:
            try:
                cams = data["cams"]
            except KeyError:
                cams = None
            # cams: {index: ___, ts: ___}
            img_cap = _write_image(cams)
        resp = {"cams": img_cap}
        return resp, 200


class SDFiles:
    def get(self, data):
        files = uos.listdir("/sd")
        # remove dotfiles
        files = [f for f in files if not f.startswith(".")]
        # {"files": ["now_2.jpg", "0_12_26_2020__11_43_10.jpg"]}
        resp = {"files": files}
        return resp, 400

    def delete(self, data):
        # e.g. "/sd/now_2.jpg"
        try:
            f_name = data["file_name"]
        except KeyError:
            f_name = None
        if f_name:
            try:
                f = open(f_name, "r")
            except OSError:
                resp = ({"message": "file not found"}, 400)
            else:
                f.close()
                uos.remove("{}".format(f_name))
                resp = ({"message": "file deleted"}, 200)
        else:
            resp = ({"message": "no `file_name` detected"}, 400)
        return resp[0], resp[1]


@app.route("/retrieve/")
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
    else:
        ts = None
        index = None

    if index is not None and ts is not None:
        fp = IMG_PATH_TEMPLATE.format(index, ts)
        await resp.send_file(fp, content_type="image/jpeg")
    else:
        msg = {"message": "index ({}) or ts ({}) missing".format(index, ts)}
        resp.code = 400
        resp.add_header("Content-Type", "application/json")
        msg_json = json.dumps(msg)
        resp.add_header("Content-Length", len(msg_json))
        await resp._send_headers()
        await resp.send(msg_json)


def run():
    logger.debug("adding resources to app")
    app.add_resource(Status, "/api/status")
    logger.debug("add resource: /api/status")
    app.add_resource(Capture, "/capture")
    logger.debug("add resource: /capture")
    app.add_resource(SDFiles, "/sd_files")
    logger.debug("add resource: /sd_files")
    logger.debug("calling app run")
    logger.to_file("/sd/mylog.json")
    app.run(host="0.0.0.0", port=8081)


if __name__ == "__main__":
    logger.debug("running as script")
    run()