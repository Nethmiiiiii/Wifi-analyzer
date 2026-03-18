from colorama import Fore, Style, init
from tabulate import tabulate
from datetime import datetime

init(autoreset=True)

SEVERITY_COLORS = {
    "CRITICAL": Fore.RED,
    "HIGH": Fore.LIGHTRED_EX,
    "MEDIUM": Fore.YELLOW,
    "LOW": Fore.CYAN,
    "INFO": Fore.GREEN,
}

def print_banner():
    print(Fore.CYAN + """
╔══════════════════════════════════════════════╗
║        🛜  Wi-Fi Security Analyzer           ║
║        Scan · Detect · Protect               ║
╚══════════════════════════════════════════════╝
""" + Style.RESET_ALL)

def print_network_info(info):
    print(Fore.CYAN + "\n📡 Connected Network Info" + Style.RESET_ALL)
    print("-" * 45)
    rows = [[k.upper(), v] for k, v in info.items()]
    print(tabulate(rows, headers=["Property", "Value"], tablefmt="rounded_outline"))

def print_devices(devices):
    print(Fore.CYAN + f"\n💻 Devices on Network ({len(devices)} found)" + Style.RESET_ALL)
    print("-" * 45)
    if devices:
        rows = [[d["ip"], d["mac"], d["hostname"]] for d in devices]
        print(tabulate(rows, headers=["IP Address", "MAC Address", "Hostname"],
                       tablefmt="rounded_outline"))
    else:
        print("  No devices found (try running as Administrator/root)")

def print_issues(issues, score):
    print(Fore.CYAN + "\n🔍 Vulnerability Report" + Style.RESET_ALL)
    print("-" * 45)

    if not issues:
        print(Fore.GREEN + "✅ No issues found!" + Style.RESET_ALL)
        return

    for i, issue in enumerate(issues, 1):
        color = SEVERITY_COLORS.get(issue["severity"], Fore.WHITE)
        print(f"\n  {color}[{issue['severity']}] {issue['issue']}{Style.RESET_ALL}")
        print(f"  📋 {issue['detail']}")
        print(f"  🔧 Fix: {Fore.GREEN}{issue['fix']}{Style.RESET_ALL}")

    # Security Score
    print("\n" + "=" * 45)
    if score >= 85:
        color = Fore.GREEN
        label = "GOOD"
    elif score >= 60:
        color = Fore.YELLOW
        label = "FAIR"
    else:
        color = Fore.RED
        label = "POOR"

    print(f"  🔐 Security Score: {color}{score}/100 — {label}{Style.RESET_ALL}")
    print("=" * 45)

def save_report(network_info, devices, issues, score, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wifi_report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write("Wi-Fi Security Analyzer Report\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        f.write("=== Network Info ===\n")
        for k, v in network_info.items():
            f.write(f"  {k}: {v}\n")

        f.write(f"\n=== Devices ({len(devices)}) ===\n")
        for d in devices:
            f.write(f"  {d['ip']} | {d['mac']} | {d['hostname']}\n")

        f.write(f"\n=== Issues ({len(issues)}) ===\n")
        for issue in issues:
            f.write(f"  [{issue['severity']}] {issue['issue']}\n")
            f.write(f"    {issue['detail']}\n")
            f.write(f"    Fix: {issue['fix']}\n\n")

        f.write(f"Security Score: {score}/100\n")

    print(Fore.GREEN + f"\n📄 Report saved to: {filename}" + Style.RESET_ALL)
    return filename