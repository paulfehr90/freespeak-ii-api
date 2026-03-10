#!/bin/bash
# FreeSpeak II Status Check
# Shows antenna status, online beltpacks, and battery levels
#
# Usage: ./status.sh [HOST] [USERNAME] [PASSWORD]

HOST="${1:-192.168.1.100}"
USER="${2:-admin}"
PASS="${3:-admin}"
BASE="http://${HOST}"

echo "=== FreeSpeak II Status ==="
echo "Host: ${HOST}"
echo ""

# Device info
echo "--- Device ---"
curl -s --digest -u "${USER}:${PASS}" "${BASE}/api/1/devices/" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for d in data:
    print(f\"  {d['device_label']} (FW: {d['versionSW']})\")
    print(f\"  Usage: {d['device_usage']}%  Power: {d['device_liveStatus'].get('power','?')}/4\")
" 2>/dev/null

echo ""

# Antennas
echo "--- Antennas ---"
curl -s --digest -u "${USER}:${PASS}" "${BASE}/api/1/devices/1/endpoints/" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
antennas = [e for e in data if e['type'] == 'FSII-Antenna']
for a in antennas:
    status = a.get('liveStatus', {}).get('status', 'unknown')
    icon = 'ON ' if status == 'online' else 'OFF'
    print(f\"  [{icon}] {a['label']:<20} FW: {a.get('versionSW', '?')}\")
print(f\"  Total: {len(antennas)} | Online: {sum(1 for a in antennas if a.get('liveStatus',{}).get('status')=='online')}\")
" 2>/dev/null

echo ""

# Beltpacks
echo "--- Beltpacks ---"
curl -s --digest -u "${USER}:${PASS}" "${BASE}/api/1/devices/1/endpoints/" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
bps = [e for e in data if e['type'] == 'FSII-BP']
online = [b for b in bps if b.get('liveStatus',{}).get('status') == 'online']
offline_with_role = [b for b in bps if b.get('liveStatus',{}).get('status') != 'online' and b.get('role')]

if online:
    print('  Online:')
    for b in online:
        ls = b.get('liveStatus', {})
        role = b.get('role', {}).get('label', 'unassigned')
        batt = ls.get('batteryLevel', '?')
        rssi = ls.get('RSSI', '?')
        lq = ls.get('linkQuality', '?')
        longevity = ls.get('longevity', {})
        time_left = f\"{longevity.get('hours','?')}h{longevity.get('minutes','?')}m\" if longevity else '?'
        print(f\"    {role:<16} Batt: {batt}%  RSSI: {rssi}  LQ: {lq}%  Remaining: {time_left}\")
else:
    print('  No beltpacks online')

print(f\"  Total registered: {len(bps)} | Online: {len(online)}\")
" 2>/dev/null

echo ""

# Active channels
echo "--- Active Channels ---"
curl -s --digest -u "${USER}:${PASS}" "${BASE}/api/1/connections/liveStatus" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
active = [c for c in data if c.get('participants')]
if active:
    for c in active:
        parts = ', '.join(p['label'] for p in c['participants'])
        print(f\"  {c['label']:<16} [{c['type']}] {parts}\")
else:
    print('  No active channels')
" 2>/dev/null
