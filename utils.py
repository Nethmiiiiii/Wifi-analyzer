import os
import platform
import subprocess

def get_os():
    return platform.system()

def is_admin():
    """Check if running with admin/root privileges"""
    try:
        if get_os() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return f"Error: {e}"

def get_wifi_interfaces():
    """Get available wireless interfaces"""
    os_name = get_os()
    interfaces = []

    if os_name == "Windows":
        output = run_command("netsh wlan show interfaces")
        for line in output.splitlines():
            if "Name" in line and "Interface" not in line:
                iface = line.split(":")[-1].strip()
                interfaces.append(iface)
    elif os_name == "Linux":
        output = run_command("iwconfig 2>/dev/null | grep 'IEEE'")
        for line in output.splitlines():
            interfaces.append(line.split()[0])
    elif os_name == "Darwin":  # macOS
        output = run_command(
            "networksetup -listallhardwareports | grep -A1 Wi-Fi | grep Device"
        )
        for line in output.splitlines():
            interfaces.append(line.split()[-1])

    return interfaces if interfaces else ["Wi-Fi", "wlan0", "en0"]