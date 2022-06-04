from hook import system

import subprocess
import binascii
import random
import json
import uuid
import time
import re
import os

TIKTOK_DEVICE_PARAMS = "ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=240702&version_name=24.7.2&device_platform=android&ab_version=24.7.2&ssmix=a&device_type={}&device_brand={}&language=en&os_api=25&os_version=7.1.2&openudid={}&manifest_version_code=2022407020&resolution={}&dpi={}&update_version_code=2022407020&app_type=normal&sys_region=US&mcc_mnc={}&timezone_name=America/New_York&carrier_region_v2={}&timezone_offset=-25200&build_number=24.7.2&region=US&uoo=0&app_language=en&carrier_region=US&locale=en&op_region=US&ac2=wifi&host_abi=x86&cdid={}&tt_data=a&okhttp_version=4.1.89.1-tiktok"
TIKTOK_API_USER_AGENT = "com.zhiliaoapp.musically/2022405010 (Linux; U; Android 7.1.2; en; {}; Build/{};tt-ok/3.12.13.1)"

def TTEncrypt(device):
    native = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"), "native")
    owd = os.getcwd()
    os.chdir(native)

    jni_path = os.path.join(os.path.join(native,"prebuilt"), system)

    command = r"java -jar -Djna.library.path={} -Djava.library.path={} unidbg.jar {}".format(jni_path, jni_path, device)
    stdout, _ = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True).communicate()
    #print(command)
    os.chdir(owd)

    return convert_hex(re.search(r'hex=([\s\S]*?)\nsize', stdout.decode()).group(1))

def convert_hex(str):
    return binascii.unhexlify(str.encode('utf-8'))

def random_deivce():
    with open("./data/devices.json") as file:
        return random.choice(json.load(file))

def random_carrier():
    with open("./data/carriers.json") as file:
        return random.choice(json.load(file))

def generate_device_uuid():
    return str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()),

def create_agent(device_brand):
    return TIKTOK_API_USER_AGENT.format(device_brand, device_brand)

def create_device():
    device = random_deivce()
    carrier = random_carrier()

    device_openudid, device_clientudid, device_googleaid, device_cdid = generate_device_uuid()

    java_log = [device_openudid, device[1], device[0], device[2], device[3], '"{}"'.format(carrier[2]), carrier[0] + carrier[1], device_clientudid, device_googleaid, device_cdid, str(int(time.time() * 1000))]
    device_params = TIKTOK_DEVICE_PARAMS.format(device[1], device[2], device_openudid, device[2], device[3], carrier[0] + carrier[1], carrier[0], device_cdid)
    device_user_agent = TIKTOK_API_USER_AGENT.format(device[1], device[1])

    return java_log, device_params, device_user_agent
