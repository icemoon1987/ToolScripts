#! -*- coding: utf8 -*-
import json
import flask
from flask import request, make_response, redirect
from baidu_netdisk_api import BaiduNetDiskAPI

app = flask.Flask(__name__)
netdisk_api = BaiduNetDiskAPI()


@app.route("/login", methods=["GET"])
def login():
    url = netdisk_api.generate_user_code_url(force_login=request.values.get("force", 0))
    return redirect(url)


@app.route("/auth", methods=["GET", "POST"])
def auth(*args, **kwargs):
    response = netdisk_api.get_access_token(user_code=request.values["code"])
    print(json.dumps(response))
    result = {
        "errno": 0,
        "errmsg": "",
    }
    if "error" in response:
        result["errno"] = 1
        result["errmsg"] = "Get Access Token Failed"
        result["traceback"] = "Baidu Response(errno=%s, errmsg=%s)" % (response["error"], response["error_description"])
        return json.dumps(result)
    netdisk_api.access_token = response["access_token"]
    result["errmsg"] = "Baidu Netdisk Auth Successfully"
    return json.dumps(result)


@app.route("/user_info", methods=["GET"])
def user_info():
    info = netdisk_api.get_user_info()
    return json.dumps(info)


@app.route("/file_list", methods=["GET"])
def file_list():
    files = netdisk_api.get_file_list()
    return json.dumps(files)


@app.route("/file_detail", methods=["GET"])
def file_detail():
    file_detail = netdisk_api.get_file_detail(request.args["fsids"], "/", True, True, True)
    return json.dumps(file_detail)


def main():
    app.run(host="localhost", port=8088, debug=True)


if __name__ == '__main__':
    main()