import platform
import frida
import color
import time

def get_system():
    if platform.system().startswith("Win"):
        print("{} Windows OS Detected!".format(color.SUCCESS))
        return "win" + platform.machine()[-2:]
    print("{} OS Unsupported!".format(color.ERROR))
    return exit(0)

def load_device():
    device = frida.get_usb_device(timeout = 5)
    print("{} Device: {}".format(color.SUCCESS, device.name))
    return device

def start_hook(): # Attach Frida to TikTok APKD
    device = load_device()
    try:
        process_id = device.spawn(["com.zhiliaoapp.musically"])
        device.resume(process_id)
        session = device.attach(process_id)
        print("{} Launched TikTok successfully!".format(color.SUCCESS))
        return session

    except frida.NotSupportedError:
        print("{} Failed to locate TikTok - Please verify the APK".format(color.ERROR))
        exit(0)

system = get_system()