import subprocess
import platform
import psutil
import requests
import win32api
import getmac
import socket
import speedtest
from screeninfo import get_monitors
import wmi
import math

def run_command(command):
    return subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True).stdout.strip()

def get_network_info():
    mac_address = getmac.get_mac_address()
    public_ip = socket.gethostbyname(socket.gethostname())
    return f'MAC Address: {mac_address}, Public IP: {public_ip}'

def get_installed_software():
    software_info = run_command('wmic product get name,version') or "No installed software found."
    return software_info

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 10**6
    upload_speed = st.upload() / 10**6
    return f'Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps'

def get_screen_resolution():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

def get_cpu_info():
    return platform.processor(), psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)

def get_gpu_model():
    try:
        gpu_info = wmi.WMI().Win32_VideoController()[0].name
        return gpu_info
    except Exception as e:
        return None

def get_ram_size():
    return round(psutil.virtual_memory().total / (1024**3), 2)

def get_screen_size():
    monitors = get_monitors()
    sizes = set((monitor.width, monitor.height) for monitor in monitors)
    return ', '.join(f"{width}x{height}" for width, height in sizes)

def get_mac_address():
    return getmac.get_mac_address()

def get_public_ip_address():
    return requests.get("https://api.ipify.org").text

def get_windows_version():
    return platform.platform()

def main():
    system_info = {
        "Installed Software": get_installed_software(),
        "Internet Speed": get_internet_speed(),
        "Screen Resolution": get_screen_resolution(),
        "CPU Model": get_cpu_info()[0],
        "CPU Cores": get_cpu_info()[1],
        "CPU Threads": get_cpu_info()[2],
        "GPU Model": get_gpu_model(),
        "RAM Size": get_ram_size(),
        "Screen Size": get_screen_size(),
        "MAC Address": get_mac_address(),
        "Public IP Address": get_public_ip_address(),
        "Windows Version": get_windows_version()
    }

    for key, value in system_info.items():
        print(f"{key}:\n{value}\n")

if __name__ == "__main__":
    main()
