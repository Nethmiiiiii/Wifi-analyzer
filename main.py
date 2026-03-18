import sys
from utils import is_admin, get_wifi_interfaces
from scanner import get_connected_network_info, scan_nearby_networks, get_connected_devices
from analyzer import full_analysis
from reporter import print_banner, print_network_info, print_devices, print_issues, save_report
from colorama import Fore, Style


def main():
    print_banner()

    # Check privileges
    if not is_admin():
        print(Fore.YELLOW +
              "⚠️  Warning: Run as Administrator/root for full functionality.\n" +
              Style.RESET_ALL)

    # Show available interfaces
    interfaces = get_wifi_interfaces()
    print(Fore.CYAN + f"📶 Detected interfaces: {', '.join(interfaces)}" + Style.RESET_ALL)

    print(Fore.WHITE + "\n[1/4] Fetching connected network info..." + Style.RESET_ALL)
    network_info = get_connected_network_info()
    print_network_info(network_info)

    print(Fore.WHITE + "\n[2/4] Scanning nearby networks..." + Style.RESET_ALL)
    nearby = scan_nearby_networks()
    print(f"  Found {len(nearby)} nearby network(s).")

    print(Fore.WHITE + "\n[3/4] Scanning for connected devices..." + Style.RESET_ALL)
    devices = get_connected_devices()
    print_devices(devices)

    print(Fore.WHITE + "\n[4/4] Running vulnerability analysis..." + Style.RESET_ALL)
    issues, score = full_analysis(network_info, nearby, devices)
    print_issues(issues, score)

    # Ask to save report
    save = input(Fore.CYAN + "\n💾 Save report to file? (y/n): " + Style.RESET_ALL)
    if save.strip().lower() == 'y':
        save_report(network_info, devices, issues, score)

    print(Fore.CYAN + "\n✅ Scan complete. Stay secure!\n" + Style.RESET_ALL)


if __name__ == "__main__":
    main()