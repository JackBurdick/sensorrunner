from urllib.parse import urlencode
import json
import requests
from secrets import IP_ADDR_STR, PORT_STR

# body_dict = {"cams": {"a": {"index": 0, "ts": "12_26_2020__11_43_10"}}}
def _build_req(ip_addr, port, api_v, api_endpoint, qs_dict, data_dict):
    URL = f"http://{ip_addr}:{port}/api/{api_v}/{api_endpoint}"

    if qs_dict is not None:
        qstr = urlencode(qs_dict)
        URL = f"{URL}?{qstr}"

    if data_dict:
        data_payload = json.dumps(data_dict)
        headers = {"Content-Type": "application/json"}
    else:
        data_payload = None
        headers = None

    return (URL, headers, data_payload)


def _v1_req_adapter(api_endpoint, qs_dict=None, data_dict=None):
    if data_dict is None:
        data_dict = {}
    r_url, r_header, r_payload = _build_req(
        ip_addr=IP_ADDR_STR,
        port=PORT_STR,
        api_v="v1",
        api_endpoint=api_endpoint,
        qs_dict=qs_dict,
        data_dict=data_dict,
    )
    return r_url, r_header, r_payload


def get_image(bucket, index, ts):
    qs_dict = {"bucket": bucket, "index": index, "ts": ts}
    r_url, r_header, r_payload = _v1_req_adapter(
        api_endpoint="retrieve", qs_dict=qs_dict
    )
    r_method = "GET"
    rd = {"method": r_method, "url": r_url, "headers": r_header, "data": r_payload}
    return rd


def capture_image(bucket, index, ts):
    data_dict = {"cam": {"bucket": bucket, "index": index, "ts": ts}}
    r_url, r_header, r_payload = _v1_req_adapter(
        api_endpoint="capture", data_dict=data_dict
    )
    r_method = "POST"
    rd = {"method": r_method, "url": r_url, "headers": r_header, "data": r_payload}
    return rd


def list_sd_files():
    r_url, r_header, r_payload = _v1_req_adapter(api_endpoint="sdfiles")
    r_method = "GET"
    rd = {"method": r_method, "url": r_url, "headers": r_header, "data": r_payload}
    return rd


def delete_sd_image(bucket, index, ts):
    qs_dict = {"bucket": bucket, "index": index, "ts": ts}
    r_url, r_header, r_payload = _v1_req_adapter(
        api_endpoint="sdfiles", qs_dict=qs_dict
    )
    r_method = "DELETE"
    rd = {"method": r_method, "url": r_url, "headers": r_header, "data": r_payload}
    return rd


def status():
    r_url, r_header, r_payload = _v1_req_adapter(api_endpoint="status")
    r_method = "GET"
    rd = {"method": r_method, "url": r_url, "headers": r_header, "data": r_payload}
    return rd


def obtain_image(bucket, index, ts):
    # url = "http://<>/api/v1/obtain?index=0&ts=01_01_2021__13_52_10&bucket=0"
    qs_dict = {"bucket": bucket, "index": index, "ts": ts}
    r_url, r_header, r_payload = _v1_req_adapter(api_endpoint="obtain", qs_dict=qs_dict)
    r_method = "GET"
    rd = {"method": r_method, "url": r_url, "headers": r_header, "data": r_payload}
    return rd


# stream=True
req_dict = obtain_image(0, 0, "01_01_2021__13_52_10")
response = requests.request(**req_dict)
# ConnectionError

print(response.status_code)
print("****" * 8)
path = "./cur_img.jpg"
if response.status_code == 200:
    with open(path, "wb") as f:
        for chunk in response:
            f.write(chunk)


# print(response.encoding)
# print(response.__dict__)
# if response.encoding == "application/json":
#     print(response.text)
