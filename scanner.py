import socket
import subprocess
import platform
from utils import run_command, get_os

def get_connected_network_info():
    """Get info about currently connected Wi-Fi network"""
    os_name = get_os()
    info = {
        "ssid": "Unknown",
        "bssid": "Unknown",
        "signal": "Unknown",
        "security": "Unknown",
        "frequency": "Unknown",
        "channel": "Unknown"
    }

    if os_name == "Windows":
        output = run_command("netsh wlan show interfaces")
        for line in output.splitlines():
            line = line.strip()
            if "SSID" in line and "BSSID" not in line:
                info["ssid"] = line.split(":")[-1].strip()
            elif "BSSID" in line:
                info["bssid"] = line.split(":", 1)[-1].strip()
            elif "Signal" in line:
                info["signal"] = line.split(":")[-1].strip()
            elif "Authentication" in line:
                info["security"] = line.split(":")[-1].strip()
            elif "Channel" in line:
                info["channel"] = line.split(":")[-1].strip()

    elif os_name == "Linux":
        output = run_command("iwconfig 2>/dev/null")
        for line in output.splitlines():
            if "ESSID" in line:
                info["ssid"] = line.split('"')[1] if '"' in line else "Unknown"
            elif "Access Point" in line:
                info["bssid"] = line.split("Access Point:")[-1].strip()
            elif "Signal level" in line:
                info["signal"] = line.split("Signal level=")[-1].split()[0]

    elif os_name == "Darwin":
        output = run_command(
            "/System/Library/PrivateFrameworks/Apple80211.framework/"
            "Versions/Current/Resources/airport -I"
        )
        for line in output.splitlines():
            line = line.strip()
            if " SSID:" in line:
                info["ssid"] = line.split(":")[-1].strip()
            elif "BSSID" in line:
                info["bssid"] = line.split(":")[-1].strip()
            elif "agrCtlRSSI" in line:
                info["signal"] = line.split(":")[-1].strip() + " dBm"
            elif "channel" in line.lower():
                info["channel"] = line.split(":")[-1].strip()

    return info

def scan_nearby_networks():
    """Scan for nearby Wi-Fi networks"""
    os_name = get_os()
    networks = []

    if os_name == "Windows":
        output = run_command("netsh wlan show networks mode=bssid")
        current = {}
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("SSID") and "BSSID" not in line:
                if current:
                    networks.append(current)
                current = {"ssid": line.split(":", 1)[-1].strip()}
            elif "Authentication" in line:
                current["security"] = line.split(":", 1)[-1].strip()
            elif "Encryption" in line:
                current["encryption"] = line.split(":", 1)[-1].strip()
            elif "Signal" in line:
                current["signal"] = line.split(":", 1)[-1].strip()
            elif "BSSID" in line:
                current["bssid"] = line.split(":", 1)[-1].strip()
        if current:
            networks.append(current)

    elif os_name == "Linux":
        output = run_command("sudo iwlist scan 2>/dev/null")
        current = {}
        for line in output.splitlines():
            line = line.strip()
            if "Cell" in line and "Address" in line:
                if current:
                    networks.append(current)
                current = {"bssid": line.split("Address:")[-1].strip()}
            elif "ESSID" in line:
                current["ssid"] = line.split('"')[1] if '"' in line else "Hidden"
            elif "Encryption key" in line:
                current["encryption"] = line.split(":")[-1].strip()
            elif "IE: IEEE 802.11i" in line or "WPA" in line:
                current["security"] = line.strip()
            elif "Signal level" in line:
                current["signal"] = line.split("Signal level=")[-1].split()[0]
        if current:
            networks.append(current)

    return networks

def get_connected_devices():
    """Get devices connected to the local network using ARP"""
    os_name = get_os()
    devices = []

    if os_name == "Windows":
        output = run_command("arp -a")
    else:
        output = run_command("arp -n")

    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0]
            mac = parts[1] if os_name != "Windows" else parts[1]
            # Filter out header lines and broadcast
            if (
                "." in ip
                and ip not in ["Address", "Interface"]
                and not ip.startswith("224.")
                and not ip.endswith(".255")
            ):
                try:
                    # Try to resolve hostname
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = "Unknown"
                    devices.append({
                        "ip": ip,
                        "mac": mac if "-" in mac or ":" in mac else "Unknown",
                        "hostname": hostname
                    })
                except:
                    pass

    return devices