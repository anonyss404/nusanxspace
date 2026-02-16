import os
import sys
import platform
import socket
import requests
import json

def get_device_id():
    try:
        return socket.gethostname()
    except:
        return "unknown"

def get_os_info():
    return platform.system() + " " + platform.release()

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=2).text
    except:
        return "0.0.0.0"

def check_lock():
    return os.path.exists("/data/local/tmp/.nusan_lock")
