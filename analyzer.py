def analyze_security_protocol(security_info):
    """Analyze the security protocol used"""
    issues = []
    score = 100

    security = security_info.get("security", "").upper()
    encryption = security_info.get("encryption", "").upper()

    # Check for open networks
    if "OPEN" in security or security == "" or security == "NONE":
        issues.append({
            "severity": "CRITICAL",
            "issue": "Open Network - No Encryption",
            "detail": "Network has no password or encryption. All traffic is visible.",
            "fix": "Enable WPA3 or WPA2 encryption immediately."
        })
        score -= 60

    # Check for WEP (broken encryption)
    elif "WEP" in security or "WEP" in encryption:
        issues.append({
            "severity": "CRITICAL",
            "issue": "WEP Encryption Detected",
            "detail": "WEP is broken and can be cracked in minutes using free tools.",
            "fix": "Upgrade router firmware and switch to WPA2 or WPA3."
        })
        score -= 50

    # Check for WPA (old)
    elif "WPA2" not in security and "WPA3" not in security and "WPA" in security:
        issues.append({
            "severity": "HIGH",
            "issue": "WPA (TKIP) Detected",
            "detail": "WPA with TKIP is outdated and vulnerable to attacks.",
            "fix": "Upgrade to WPA2-AES or WPA3."
        })
        score -= 30

    # WPA2 is acceptable
    elif "WPA2" in security:
        if "TKIP" in encryption:
            issues.append({
                "severity": "MEDIUM",
                "issue": "WPA2 with TKIP Cipher",
                "detail": "TKIP cipher is weaker than AES/CCMP.",
                "fix": "Switch cipher to AES/CCMP in router settings."
            })
            score -= 15
        else:
            issues.append({
                "severity": "INFO",
                "issue": "WPA2-AES Detected",
                "detail": "WPA2 with AES is secure but WPA3 is recommended.",
                "fix": "Consider upgrading to WPA3 if your router supports it."
            })
            score -= 5

    # WPA3 is the best
    elif "WPA3" in security:
        issues.append({
            "severity": "INFO",
            "issue": "WPA3 Detected",
            "detail": "Excellent! WPA3 is the latest and most secure standard.",
            "fix": "No action needed."
        })

    return issues, max(0, score)


def analyze_signal_strength(signal_str):
    """Analyze Wi-Fi signal strength"""
    issues = []

    try:
        signal = int(''.join(filter(lambda x: x.isdigit() or x == '-', signal_str)))
        if signal < -80:
            issues.append({
                "severity": "MEDIUM",
                "issue": "Weak Signal Strength",
                "detail": f"Signal is {signal} dBm. Weak signals can cause performance issues.",
                "fix": "Move closer to router or add a Wi-Fi extender."
            })
        elif signal < -70:
            issues.append({
                "severity": "LOW",
                "issue": "Moderate Signal Strength",
                "detail": f"Signal is {signal} dBm. Could be stronger.",
                "fix": "Consider repositioning the router."
            })
    except:
        pass

    return issues


def check_suspicious_devices(devices):
    """Flag devices with suspicious MAC addresses"""
    issues = []
    known_suspicious_prefixes = [
        "00:00:00",  # Null MAC
        "ff:ff:ff",  # Broadcast
    ]

    for device in devices:
        mac = device.get("mac", "").lower()
        for prefix in known_suspicious_prefixes:
            if mac.startswith(prefix):
                issues.append({
                    "severity": "HIGH",
                    "issue": f"Suspicious Device Detected",
                    "detail": f"Device {device['ip']} has suspicious MAC: {mac}",
                    "fix": "Investigate this device and block if unrecognized."
                })

    return issues


def scan_nearby_for_evil_twin(current_ssid, nearby_networks):
    """Detect potential evil twin / rogue AP attacks"""
    issues = []
    duplicates = []

    for net in nearby_networks:
        net_ssid = net.get("ssid", "")
        if net_ssid == current_ssid:
            duplicates.append(net)

    if len(duplicates) > 1:
        issues.append({
            "severity": "HIGH",
            "issue": "Possible Evil Twin / Rogue AP Detected",
            "detail": f"Multiple networks found with SSID '{current_ssid}'. "
                      "This may indicate a man-in-the-middle attack.",
            "fix": "Verify the BSSID of your router. Avoid connecting to untrusted networks."
        })

    return issues


def full_analysis(network_info, nearby_networks, devices):
    """Run all checks and return combined results"""
    all_issues = []
    security_issues, score = analyze_security_protocol(network_info)
    all_issues.extend(security_issues)
    all_issues.extend(analyze_signal_strength(network_info.get("signal", "")))
    all_issues.extend(check_suspicious_devices(devices))
    all_issues.extend(
        scan_nearby_for_evil_twin(network_info.get("ssid"), nearby_networks)
    )

    return all_issues, score