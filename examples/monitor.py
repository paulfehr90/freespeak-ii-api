#!/usr/bin/env python3
"""
FreeSpeak II Monitor
Polls the base station and displays live status of antennas and beltpacks.

Usage:
    python3 monitor.py --host 192.168.1.100 --user admin --password admin
    python3 monitor.py --host 192.168.1.100 --user admin --password admin --interval 5

Requires: pip install requests
"""

import argparse
import json
import os
import sys
import time

try:
    import requests
    from requests.auth import HTTPDigestAuth
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests")
    sys.exit(1)


class FreeSpeak:
    def __init__(self, host, username, password):
        self.base_url = f"http://{host}"
        self.auth = HTTPDigestAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth

    def get(self, path):
        resp = self.session.get(f"{self.base_url}{path}", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def devices(self):
        return self.get("/api/1/devices/")

    def endpoints(self, device_id=1):
        return self.get(f"/api/1/devices/{device_id}/endpoints/")

    def connections(self):
        return self.get("/api/1/connections/")

    def live_status(self):
        return self.get("/api/1/connections/liveStatus")

    def roles(self):
        return self.get("/api/1/roles/")

    def interfaces(self, device_id=1):
        return self.get(f"/api/1/devices/{device_id}/interfaces/")

    def gpio(self):
        return self.get("/api/1/devices/0/gpio")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def format_bar(value, max_val=100, width=15):
    filled = int(value / max_val * width)
    return f"[{'#' * filled}{'.' * (width - filled)}] {value}%"


def display_status(fs):
    clear_screen()

    # Device info
    devices = fs.devices()
    dev = devices[0] if devices else {}
    print(f"{'=' * 70}")
    print(f"  FreeSpeak II: {dev.get('device_label', '?')}  |  "
          f"FW: {dev.get('versionSW', '?')}  |  "
          f"Usage: {dev.get('device_usage', '?')}%")
    print(f"{'=' * 70}")

    # Endpoints
    endpoints = fs.endpoints()
    antennas = [e for e in endpoints if e["type"] == "FSII-Antenna"]
    beltpacks = [e for e in endpoints if e["type"] == "FSII-BP"]

    # Antennas
    print(f"\n  ANTENNAS ({sum(1 for a in antennas if a.get('liveStatus', {}).get('status') == 'online')}/{len(antennas)} online)")
    print(f"  {'-' * 50}")
    for ant in antennas:
        status = ant.get("liveStatus", {}).get("status", "unknown")
        icon = " ON" if status == "online" else "OFF"
        freq = ant.get("liveStatus", {}).get("frequencyType", "?")
        fw = ant.get("versionSW", "?")
        print(f"  [{icon}]  {ant['label']:<22} {freq} GHz   FW {fw}")

    # Beltpacks
    online_bps = [b for b in beltpacks if b.get("liveStatus", {}).get("status") == "online"]
    print(f"\n  BELTPACKS ({len(online_bps)}/{len(beltpacks)} online)")
    print(f"  {'-' * 66}")

    if online_bps:
        print(f"  {'Role':<14} {'Battery':<22} {'RSSI':<8} {'LQ':<8} {'Remaining':<10}")
        print(f"  {'-' * 66}")
        for bp in online_bps:
            ls = bp.get("liveStatus", {})
            role = bp.get("role", {}).get("label", bp["label"])
            batt = ls.get("batteryLevel", 0)
            rssi = ls.get("RSSI", 0)
            lq = ls.get("linkQuality", 0)
            longevity = ls.get("longevity", {})
            remaining = f"{longevity.get('hours', '?')}h{longevity.get('minutes', '?'):02d}m" if longevity else "?"
            print(f"  {role:<14} {format_bar(batt)}  {rssi:<8} {lq:<8} {remaining}")
    else:
        print("  No beltpacks online")

    # Live connections
    live = fs.live_status()
    active = [c for c in live if c.get("participants")]
    print(f"\n  CHANNELS ({len(active)} active)")
    print(f"  {'-' * 50}")
    if active:
        for conn in active:
            parts = []
            for p in conn["participants"]:
                state = ""
                if "Talk" in p.get("joinState", ""):
                    state = " [TALK]"
                parts.append(f"{p['label']}{state}")
            print(f"  {conn['label']:<16} {', '.join(parts)}")
    else:
        print("  No active channels")

    print(f"\n  Last updated: {time.strftime('%H:%M:%S')}")
    print(f"  Press Ctrl+C to exit")


def main():
    parser = argparse.ArgumentParser(description="FreeSpeak II Monitor")
    parser.add_argument("--host", required=True, help="Base station IP address")
    parser.add_argument("--user", default="admin", help="Username (default: admin)")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--interval", type=int, default=3, help="Refresh interval in seconds (default: 3)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    fs = FreeSpeak(args.host, args.user, args.password)

    # Test connection
    try:
        fs.devices()
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to {args.host}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: Authentication failed — {e}")
        sys.exit(1)

    if args.once:
        display_status(fs)
        return

    try:
        while True:
            try:
                display_status(fs)
            except requests.exceptions.RequestException as e:
                print(f"\nConnection error: {e}")
                print("Retrying...")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()
