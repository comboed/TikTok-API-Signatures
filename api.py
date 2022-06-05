from device import create_device, TTEncrypt
from flask import Flask, jsonify, request
from urllib.parse import unquote
from hook import start_hook

import requests
import frida
import time
import gzip

# Device Data
DEVICE_USER_AGENT = None
DEVICE_PARAMS = None
DEVICE_IID = None
DEVICE_ID = None

# Dependent variables
running = False
script = None

session = start_hook()
app = Flask(__name__)

@app.route("/")
def index():
    return "/"

@app.route("/run/")
def inject_script():
    global running, script
    if not running:
        with open(file = "./data/sign.js", mode = "r", encoding = "UTF-8") as file:
            script = session.create_script(file.read())
            script.load()
            running = True
            return jsonify({"status_code": 0, "message": "Successfully injected script!"})

    return jsonify({"status_code": -1, "message": "Already injected script!"})

@app.route("/shutdown/")
def shutdown():
    global running
    try:
        running = False
        script.unload()
        return jsonify({"status_code": 1, "message": "Successfully destroyed script!"})
    except (frida.InvalidOperationError, AttributeError):
        return jsonify({"status_code": 2, "message": "Script already destroyed!"})

@app.route("/sign/")
def sign_api():
    try:
        url = unquote(request.url).split("/sign/?")[1]

        data = script.exports.sign(url)
        x_gorgon = data.get("X-Gorgon")
        x_khronos = data.get("X-Khronos")

        if len(x_gorgon) > 5 and len(x_khronos) > 5:
            return jsonify({"status_code": 0, "X-Gorgon": x_gorgon, "X-Khronos": x_khronos, "Endpoint": url})
        return jsonify({"status_code": 1, "message": "Unable to sign request."})

    except (frida.InvalidOperationError, AttributeError, IndexError):
        return jsonify({"status_code": -1, "message": "Script is not running!"})

@app.route("/register_device/")
def register_device():
    global DEVICE_PARAMS, DEVICE_USER_AGENT, DEVICE_IID, DEVICE_ID
    java_log, DEVICE_PARAMS, DEVICE_USER_AGENT = create_device()
    device_params = "{}&_rticket={}&ts={}".format(DEVICE_PARAMS, str((time.time() * 1000)).split('.')[0], str(time.time()).split(".")[0])

    try:
        response = requests.get("http://127.0.0.1:5000/sign/?" + unquote("https://log16-applog-useast5.us.tiktokv.com/service/2/device_register/?" + device_params)).json()
        
        response = requests.post(response["Endpoint"], data = TTEncrypt(" ".join(java_log)), headers = {
            "Content-Type": "application/octet-stream; tt-data=a",
            "X-Gorgon": response["X-Gorgon"],
            "X-Khronos": response["X-Khronos"],
            "User-Agent": DEVICE_USER_AGENT}, allow_redirects = True).json()

        if response["device_id_str"] != "0":
            DEVICE_IID, DEVICE_ID = response["install_id_str"], response["device_id_str"]
            DEVICE_PARAMS += "&iid=" + DEVICE_IID + "&device_id=" + DEVICE_ID
            #print(DEVICE_PARAMS)
            return jsonify({"status_code": 0, "data": response})
        return jsonify({"status_code": -1, "message": "Unable to register device."})

    except KeyError:
        return jsonify({"status_code": 2, "message": "Script is not running."})
    
if __name__ == "__main__":
    app.run()
