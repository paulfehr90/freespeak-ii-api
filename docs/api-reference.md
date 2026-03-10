# FreeSpeak II API Reference

> **Disclaimer:** This is unofficial documentation created through observation of the CCM web interface. Not affiliated with Clear-Com. Use at your own risk.

## Overview

- **Base URL:** `http://{BASE_STATION_IP}`
- **Auth:** HTTP Digest (`WWW-Authenticate: Digest realm="CCM"`)
- **Format:** JSON request and response bodies
- **Real-time:** Socket.IO at `/socket.io/`
- **CORS:** Enabled (`Access-Control-Allow-Origin: *`)

### Authentication

All endpoints require HTTP Digest authentication:

```bash
curl --digest -u USERNAME:PASSWORD http://{BASE_STATION_IP}/api/1/devices/
```

### Response Patterns

| Pattern | Format |
|---------|--------|
| Success (list) | JSON array `[...]` |
| Success (single) | JSON object `{...}` |
| Success (action) | `{"ok": true, "message": "..."}` |
| Error | `{"ok": false, "message": "..."}` |

---

## Devices

### `GET /api/1/devices/`

List all base stations in the system (linked groups may have multiple).

<details>
<summary>Example Response</summary>

```json
[
    {
        "device_id": 1,
        "device_label": "My Base Station",
        "device_ipAddress": "192.168.1.100",
        "isHost": true,
        "deviceType_name": "FSII",
        "device_uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "device_settings": {
            "keysets": [],
            "groups": [],
            "antennaPorts": {
                "antenna0": "rj45",
                "antenna1": "rj45"
            },
            "displayBrightness": 170,
            "aaBatteryType": "NiMH",
            "dspPlcState": "Enabled",
            "roleSorting": "RoleNumber",
            "network": {
                "staticIP": "192.168.1.100",
                "mode": "static",
                "netmask": "255.255.255.0",
                "gateway": "192.168.1.1",
                "dns1": "8.8.8.8",
                "dns2": "8.8.4.4",
                "mac": "00:0e:98:xx:xx:xx"
            },
            "wirelessId": "XXX"
        },
        "device_isMaster": true,
        "device_linking": "linkMaster",
        "device_masterStatus": "READY",
        "device_netMode": "WAN",
        "device_usage": 18,
        "device_isReachable": true,
        "device_liveStatus": {
            "gpis": [
                {"id": 0, "status": true, "forced": false}
            ],
            "gpos": [],
            "power": 4
        },
        "versionSW": "1.6.15.0 (Boot-Version FS-2.1.00)",
        "versionHW": "2-2",
        "linkingVersion": 7,
        "res": "/api/1/devices/1",
        "systemId": "0xxxxx",
        "licensedFeatures": [{"name": "25Beltpacks"}]
    }
]
```

</details>

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `device_id` | number | Unique device ID |
| `device_label` | string | User-assigned label |
| `device_ipAddress` | string | IP address |
| `deviceType_name` | string | Device type (`FSII`) |
| `device_settings.antennaPorts` | object | Antenna port types (`rj45` or `fiber`) |
| `device_settings.network` | object | Network config (IP, mask, gateway, DNS, MAC) |
| `device_settings.wirelessId` | string | Wireless system ID |
| `versionSW` | string | Firmware version |
| `versionHW` | string | Hardware version |
| `licensedFeatures` | array | Licensed features |
| `device_liveStatus.power` | number | Power level (0-4) |
| `device_usage` | number | Resource usage percentage |

### `GET /api/2/devices/`

Same response as v1. The v2 API is used for newer operations (network setup, config restore).

### `PUT /api/1/devices/{deviceId}`

Update device settings (label, display brightness, battery type, antenna ports, keysets, GPIO config).

### `GET /api/1/devices/{deviceId}/capability`

Returns device capabilities.

<details>
<summary>Example Response</summary>

```json
{
    "type": "FSII",
    "psuMonitoring": true,
    "webSocket": true,
    "labelLength": 10,
    "endpoints": true,
    "saveRestore": true,
    "upgrade": {
        "minSize": 102400,
        "maxSize": 104857600,
        "extensions": [".gz", ".fww", ".FWW"]
    },
    "network": {"dns": false},
    "licensing": true
}
```

</details>

### `GET /api/1/devices/{deviceId}/getDateTime`

```json
{"ok": true, "message": "Date and Time are --> ...", "wbsDateTime": "Wed Feb 25 04:42:04 UTC 2026\n"}
```

### `GET /api/1/devices/{deviceId}/alerts/current`

Returns array of current system alerts. Empty array `[]` when no active alerts.

### `GET /api/1/devices/{deviceId}/snapshotinfo`

Returns support snapshot creation progress: `{"percentComplete": 0}`.

### `GET /api/1/devices/{deviceId}/upgrade`

Returns firmware upgrade status: `{"percentComplete": 0, "stage": "Idle", "ok": true}`.

### `GET /api/1/devices/{deviceId}/backup`

Downloads configuration backup as binary file. Use `Accept: application/octet-stream`. Filename is in the `Content-Disposition` response header.

### Device Actions (POST)

| Endpoint | Description | Risk |
|----------|-------------|------|
| `POST /api/1/devices/{id}/reboot` | Reboot base station | High — interrupts all comms |
| `POST /api/1/devices/{id}/restartServices` | Restart services | Medium |
| `POST /api/1/devices/{id}/resettodefault` | Factory reset | **Critical — wipes everything** |
| `POST /api/1/devices/{id}/setDateTime` | Set date/time | Low |
| `POST /api/1/devices/{id}/setNetMode` | Set network mode (WAN/LAN) | Medium |
| `POST /api/1/devices/{id}/startOTA` | Start OTA beltpack update | Medium |
| `POST /api/1/devices/{id}/snapshot` | Create support snapshot | Low |
| `POST /api/1/devices/{id}/updatelinkingconfig` | Update linking config | Medium |
| `POST /api/2/devices/{id}/setupnetwork` | Configure network | Medium — may change IP |
| `POST /api/1/devices/0/upload` | Upload firmware file | Medium |
| `POST /api/2/devices/restore` | Restore config backup | High |

> **WARNING:** `resettodefault` immediately and irreversibly wipes all configuration. There is no confirmation prompt at the API level.

---

## Endpoints (Antennas & Beltpacks)

Wireless endpoints include FSII-Antenna (transceivers) and FSII-BP (beltpacks).

### `GET /api/1/devices/{deviceId}/endpoints/`

Returns all antennas and beltpacks.

**Antenna Response:**
```json
{
    "res": "/api/1/devices/1/endpoints/1000000",
    "id": 1000000,
    "device_id": 1,
    "label": "Antenna 1",
    "type": "FSII-Antenna",
    "liveStatus": {
        "status": "online",
        "frequencyType": "1.9",
        "syncState": "base"
    },
    "settings": {"syncOffset": 1},
    "versionSW": "2.7.28.0",
    "updateRequired": false
}
```

**Beltpack Response:**
```json
{
    "res": "/api/1/devices/1/endpoints/12345",
    "id": 12345,
    "device_id": 1,
    "label": "FSII-BP-12345",
    "type": "FSII-BP",
    "frequencyType": "1.9",
    "liveStatus": {
        "status": "online",
        "role": 9,
        "antennaIndex": 0,
        "antennaSlot": 3,
        "keyState": [
            {"keysetIndex": 0, "currentState": "talk+listen", "volume": 53},
            {"keysetIndex": 1, "currentState": "listen", "volume": 80},
            {"keysetIndex": 2, "currentState": "off", "volume": 0},
            {"keysetIndex": 3, "currentState": "off", "volume": 50},
            {"keysetIndex": 4, "currentState": "off", "volume": 100}
        ],
        "batteryType": "Li-Ion",
        "batteryLevel": 79,
        "RSSI": 48,
        "linkQuality": 58,
        "frameErrorRate": 0,
        "longevity": {"hours": 13, "minutes": 50}
    },
    "role": {
        "id": 9,
        "isDefault": false,
        "label": "Stage Manager",
        "res": "/api/1/roles/9"
    },
    "settings": {"default_role": 9},
    "versionSW": "5.25.32.0",
    "updateRequired": false,
    "callState": false
}
```

**Endpoint Fields:**

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `type` | string | Both | `FSII-Antenna` or `FSII-BP` |
| `liveStatus.status` | string | Both | `online`, `offline`, or `unknown` |
| `liveStatus.frequencyType` | string | Both | Frequency band (e.g. `1.9`) |
| `liveStatus.syncState` | string | Antenna | Sync state (`base`) |
| `liveStatus.batteryLevel` | number | Beltpack | Battery percentage (0-100) |
| `liveStatus.batteryType` | string | Beltpack | `Li-Ion` or `NiMH` |
| `liveStatus.RSSI` | number | Beltpack | Signal strength |
| `liveStatus.linkQuality` | number | Beltpack | Link quality (0-100) |
| `liveStatus.frameErrorRate` | number | Beltpack | Frame error rate |
| `liveStatus.longevity` | object | Beltpack | `{hours, minutes}` remaining |
| `liveStatus.antennaIndex` | number | Beltpack | Connected antenna index |
| `liveStatus.antennaSlot` | number | Beltpack | Antenna time slot |
| `liveStatus.keyState[]` | array | Beltpack | Key states with volume |
| `role` | object | Beltpack | Assigned role `{id, label}` |
| `callState` | boolean | Beltpack | Active call |

### `GET /api/1/devices/{deviceId}/endpoints/{endpointId}`

Returns a single endpoint by ID.

### `PUT /api/1/devices/{deviceId}/endpoints/{endpointId}`

Update endpoint settings (label, default role, sync offset).

### `DELETE /api/1/devices/{deviceId}/endpoints/{endpointId}`

Unregister an endpoint.

### Endpoint Actions (POST)

| Endpoint | Description |
|----------|-------------|
| `POST .../endpoints/{id}/reboot` | Remotely reboot a beltpack |
| `POST .../endpoints/{id}/rmk` | Remote Mic Kill — force microphone off |
| `POST .../endpoints/{id}/call` | Send call signaling |
| `POST .../endpoints/{id}/resettodefault` | Reset endpoint settings to defaults |

### ID Ranges

- **Antennas:** 1000000+ (1000000-1000009 observed for 10 transceivers)
- **Beltpacks:** Various numeric IDs in lower ranges

---

## Connections (Partylines & Groups)

### `GET /api/1/connections/`

Returns all partylines and groups.

```json
[
    {"id": 1, "label": "Channel 1", "res": "/api/1/connections/1", "type": "partyline"},
    {"id": 13, "label": "Group 1", "res": "/api/1/connections/13", "type": "group"}
]
```

- **Partylines:** IDs 1-12 (max 12)
- **Groups:** IDs 13-24 (max 12)

### `GET /api/1/connections/{connectionId}`

Returns a single connection.

### `GET /api/1/connections/liveStatus`

Returns all connections with real-time participant status. This is the key endpoint for monitoring active communications.

```json
[
    {
        "id": 1,
        "label": "Channel 1",
        "participants": [
            {
                "device_id": 1,
                "id": 60577542,
                "joinState": "Talk-Listen",
                "label": "Port Name",
                "res": "/api/1/devices/1/interfaces/258/ports/66049",
                "state": "connected",
                "type": "2W",
                "events": {"call": false, "talk": false, "control": false}
            }
        ],
        "type": "partyline",
        "events": {"call": false, "talk": false, "control": false}
    }
]
```

**Participant Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `joinState` | string | `Talk-Listen`, `Listen`, `Talk` |
| `label` | string | Port/device label |
| `state` | string | `connected` |
| `type` | string | `SA`, `2W`, `4W`, `HS` |
| `events.talk` | boolean | Currently talking |
| `events.call` | boolean | Active call signal |

### `PUT /api/1/connections/{connectionId}`

Update a connection. Body: `{"label": "New Name"}`.

### `POST /api/1/connections/`

Create a new partyline or group (subject to max limits).

### `DELETE /api/1/connections/{connectionId}`

Delete a connection. All ports must be removed first.

---

## Roles

Roles define beltpack configurations — channel assignments, talk/listen modes, audio settings, and alerts. Max 55 roles.

### `GET /api/1/roles/`

Returns all roles with full configuration.

<details>
<summary>Example Response</summary>

```json
[
    {
        "id": 6,
        "type": "FSII-BP",
        "label": "Default",
        "description": "",
        "isDefault": true,
        "settings": {
            "keysets": [
                {
                    "keysetIndex": 0,
                    "connections": [{"res": "/api/1/connections/1"}],
                    "activationState": "talklisten",
                    "isReplyKey": false,
                    "isCallKey": false,
                    "talkBtnMode": "latching"
                }
            ],
            "groups": [],
            "headphoneLimit": 3,
            "sidetoneGain": -9.6,
            "sidetoneControl": "tracking",
            "masterVolume": 0,
            "portInputGain": 0,
            "portOutputGain": 0,
            "micEchoCancellation": true,
            "batteryAlarmMode": "vibrate+audio",
            "lowBatteryThreshold": 25,
            "callAlertMode": "off",
            "outOfRangeAlarm": "off"
        }
    }
]
```

</details>

### `GET /api/1/roles/{roleId}`

Returns a single role with full keyset configuration.

### `POST /api/1/roles/`

Create a new role.

### `PUT /api/1/roles/{roleId}`

Update role settings.

### `DELETE /api/1/roles/{roleId}`

Delete a role.

### Keyset Activation States

| Value | Description |
|-------|-------------|
| `talk` | Talk-Only |
| `listen` | Listen-Only |
| `talklisten` | Talk & Listen |
| `dualtalklisten` | Dual Talk & Listen |
| `forcelisten` | Force Listen |
| `talkforcelisten` | Talk & Force Listen |
| `forcetalkforcelisten` | Force Talk & Force Listen |

### Talk Button Modes

| Value | Description |
|-------|-------------|
| `latching` | Toggle on/off |
| `non-latching` | Push-to-talk |
| `disabled` | Button disabled |

---

## Audio Interfaces

The base station has 5 audio interfaces.

### `GET /api/1/devices/{deviceId}/interfaces/`

```json
[
    {
        "audioInterface_hwIndex": 0,
        "audioInterface_id": 256,
        "audioInterface_portCount": 3,
        "audioInterfaceType": "FSII-E1",
        "audioInterfaceType_shortName": "E1",
        "audioInterfaceType_longName": "Station",
        "audioInterface_settings": {},
        "audioInterface_liveStatus": {
            "ports": {},
            "powerSense": false,
            "powerOn": false
        },
        "res": "/api/1/devices/1/interfaces/256"
    }
]
```

**Interface Summary:**

| hwIndex | ID | Type | Description | Ports |
|---------|-----|------|-------------|-------|
| 0 | 256 | FSII-E1 | Station | 3 (PGM, SA, HS) |
| 1 | 257 | FSII-2W | 2-Wire A | 2 |
| 2 | 258 | FSII-2W | 2-Wire B | 2 |
| 3 | 259 | FSII-4W | 4-Wire A | 2 |
| 4 | 260 | FSII-4W | 4-Wire B | 2 |

### `GET /api/1/devices/{deviceId}/interfaces/{interfaceId}`

Returns a single interface by `audioInterface_id`.

### `PUT /api/1/devices/{deviceId}/interfaces/{interfaceId}`

Update interface settings (2-wire mode: `ClearCom`/`RTS`, power on/off).

---

## Ports

> **IMPORTANT:** Port listing uses `hwIndex` (0-4), NOT `audioInterface_id` (256-260).

### `GET /api/1/devices/{deviceId}/interfaces/{hwIndex}/ports/`

```json
[
    {
        "port_hwIndex": 0,
        "port_label": "Program",
        "port_id": 65536,
        "port_connections": {},
        "port_settings": {"inputGain": -12},
        "liveStatus": {"vox": {"status": false}, "pending": false, "online": true},
        "port_config_type": "PGM"
    }
]
```

**Port ID Ranges:**

| Range | Interface |
|-------|-----------|
| 65536-65538 | Station (E1) — PGM, SA, HS |
| 65792-65793 | 2-Wire Interface A |
| 66048-66049 | 2-Wire Interface B |
| 66304-66305 | 4-Wire Interface A |
| 66560-66561 | 4-Wire Interface B |

### `PUT /api/1/devices/{deviceId}/interfaces/{interfaceId}/ports/{portId}`

Update port settings (gain, termination, call signal, serial config for 4W).

### Port Actions (POST)

| Endpoint | Body | Description |
|----------|------|-------------|
| `.../ports/{id}/join` | `{"target": "/api/1/connections/{id}"}` | Associate port with connection |
| `.../ports/{id}/leave` | `{"target": "/api/1/connections/{id}"}` | Remove port from connection |
| `.../ports/{id}/gpo` | `{"enabled": true, "timeout": 4000}` | Set GPO state |
| `.../ports/{id}/nulling` | — | Start line nulling (2-wire) |

### `GET .../ports/{portId}/nulling`

Returns nulling status: `{"ok": true, "nulling": "Idle"}`.

### SIP Calls

| Endpoint | Method | Description |
|----------|--------|-------------|
| `.../ports/{id}/calls/` | GET | List active calls |
| `.../ports/{id}/calls/` | POST | Make call — `{"uri": "sip:..."}` |
| `.../ports/{id}/calls/{callId}` | DELETE | Hang up call |

---

## GPIO

2 General Purpose Inputs (GPI) and 4 General Purpose Outputs (GPO).

### `GET /api/1/devices/0/gpio`

Returns all GPIO. `type=0` is GPI, `type=1` is GPO.

```json
[
    {
        "id": 0, "device_id": 1, "label": "GPI1", "type": 0,
        "liveStatus": {"id": 0, "status": true, "forced": false},
        "settings": {"events": []}
    },
    {
        "id": 0, "device_id": 1, "label": "GPO1", "type": 1,
        "liveStatus": {},
        "settings": {"events": [], "offDelays": 0}
    }
]
```

### GPI Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/devices/{id}/gpi/{gpiId}` | PUT | Update GPI settings |
| `/api/1/devices/{id}/gpi/{gpiId}/addEvent` | POST | Add event trigger |
| `/api/1/devices/{id}/gpi/{gpiId}/events/{eventId}` | PUT | Update event |
| `/api/1/devices/{id}/gpi/{gpiId}/events/{eventId}` | DELETE | Remove event |

### GPO Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/devices/{id}/gpo/{gpoId}` | PUT | Update GPO settings |
| `/api/1/devices/{id}/gpo/{gpoId}/addEvent` | POST | Add event trigger |
| `/api/1/devices/{id}/gpo/{gpoId}/events/{eventId}` | PUT | Update event |
| `/api/1/devices/{id}/gpo/{gpoId}/events/{eventId}` | DELETE | Remove event |

---

## External Devices (SIP / IVC-32)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/externalDevices/` | GET | List all |
| `/api/1/externalDevices/` | POST | Add new |
| `/api/1/externalDevices/{id}` | GET | Get one |
| `/api/1/externalDevices/{id}` | PUT | Update |
| `/api/1/externalDevices/{id}` | DELETE | Remove |
| `/api/1/externalDevices/{id}/ports/{portId}` | POST | Add port |
| `/api/1/externalDevices/{id}/ports/{portId}` | PUT | Update port |
| `/api/1/externalDevices/{id}/ports/{portId}` | DELETE | Remove port |

---

## IVP Users

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/ivpusers/` | GET | List all |
| `/api/1/ivpusers/` | POST | Create |
| `/api/1/ivpusers/{userId}` | GET | Get one |
| `/api/1/ivpusers/{userId}` | PUT | Update |
| `/api/1/ivpusers/{userId}` | DELETE | Remove |

---

## Users & Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/users/` | GET | List users |
| `/api/1/users/{username}` | GET | Get user |
| `/api/1/users/{username}` | PUT | Update user/password |

---

## Capabilities

### `GET /api/1/capabilities/linkgroup`

```json
{
    "roles": [{"type": "FSII-BP", "title": "Beltpack (FSII)", "labelLength": 10}],
    "maxRoles": 55,
    "codec": "Opus",
    "connections": [
        {"type": "partyline", "labelLength": 10, "max": 12, "dynamic": false},
        {"type": "group", "labelLength": 10, "max": 12, "dynamic": false}
    ]
}
```

### `GET /api/1/capabilities/interfaces/{type}`

Supported types: `FSII-2W`, `FSII-4W`. (`FSII-E1` returns an error.)

```json
{"type": "FSII-2W", "fec": false, "networkQuality": false, "power": true, "mode": true, "termination": true, "callSignal": true}
```

### `GET /api/1/capabilities/devices/{type}`

Use type `FSII`.

---

## Events / Logging

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/events/{entityId}` | GET | Get paginated event log |
| `/api/1/events/export/{entityId}` | GET | Export all events |
| `/api/1/devices/{id}/networkEvent/{eventId}` | PUT | Update network event |

Event log response: `{"desiredEvents": [], "totalNumberOfEvents": 0, "totalNumberOfPages": null}`

---

## Licensing

The base station uses WIBU-SYSTEMS CodeMeter for license management.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/1/devices/{id}/license/context` | GET | Download license request file |
| `/api/1/devices/{id}/license/upload` | POST | Upload license activation file |
| `/api/1/devices/{id}/license/ticket/{ticketId}` | GET | Get license ticket info |
| `/api/1/devices/{id}/updateLicensePasscode` | POST | Update license passcode |
| `/api/1/devices/{id}/wibuUpdate` | POST | WIBU license update |

---

## Socket.IO Real-Time Events

Connect to `http://{BASE_STATION_IP}/socket.io/` for real-time updates.

```bash
# Verify Socket.IO is available
curl "http://{BASE_STATION_IP}/socket.io/?EIO=3&transport=polling"
# Returns: {"sid":"...","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":60000}
```

### Client → Server (Emit)

| Event | Data | Description |
|-------|------|-------------|
| `EndpointInit` | — | Request endpoint initialization |
| `GpiInit` | — | Request GPI initialization |
| `GpoInit` | — | Request GPO initialization |
| `live:update` | `{topic: "start"}` | Subscribe to a live topic |
| `live:update` | `{topic: "stop"}` | Unsubscribe from a live topic |

### Server → Client (On)

| Event | Description |
|-------|-------------|
| `EndpointInit` | Endpoint initialization data |
| `EndpointAdded` | New beltpack/antenna registered |
| `EndpointRemoved` | Endpoint removed |
| `EndpointUpdated` | Endpoint state changed (battery, RSSI, status) |
| `GpiInit` | GPI initialization data |
| `GpiUpdated` | GPI state changed |
| `GpiEventAdded` | GPI event added |
| `GpiEventRemoved` | GPI event removed |
| `GpiEventUpdated` | GPI event updated |
| `GpoInit` | GPO initialization data |
| `GpoUpdated` | GPO state changed |
| `GpoEventAdded` | GPO event added |
| `GpoEventRemoved` | GPO event removed |
| `GpoEventUpdated` | GPO event updated |

### Live Topics

Subscribe via `emit("live:update", {topic: "start"})`:

| Topic | Description |
|-------|-------------|
| `live:alerts` | Alert notifications |
| `live:calls` | Call state changes |
| `live:connections` | Connection/partyline updates |
| `live:devices` | Device status updates |
| `live:endpoints` | Beltpack/antenna status changes |
| `live:eventLog` | Event log entries |
| `live:externalDevices` | External device updates |
| `live:gpios` | GPIO state changes |
| `live:interfaces` | Audio interface updates |
| `live:ivpusers` | IVP user updates |
| `live:linkgroupcapabilities` | Link group capability changes |
| `live:ports` | Port status updates |
| `live:roles` | Role configuration changes |
| `live:statistics` | Statistics/metrics |
| `live:vpl` | Virtual Party Line updates |

---

## Complete Endpoint Reference

### API v1

| Endpoint | GET | POST | PUT | DELETE |
|----------|-----|------|-----|--------|
| `/api/1/devices/` | List | — | — | — |
| `/api/1/devices/{id}` | Get | — | Update | — |
| `/api/1/devices/{id}/capability` | Caps | — | — | — |
| `/api/1/devices/{id}/getDateTime` | DateTime | — | — | — |
| `/api/1/devices/{id}/alerts/current` | Alerts | — | — | — |
| `/api/1/devices/{id}/snapshotinfo` | Progress | — | — | — |
| `/api/1/devices/{id}/upgrade` | Status | Execute | — | — |
| `/api/1/devices/{id}/backup` | Download | — | — | — |
| `/api/1/devices/{id}/reboot` | — | Reboot | — | — |
| `/api/1/devices/{id}/restartServices` | — | Restart | — | — |
| `/api/1/devices/{id}/resettodefault` | — | **Reset** | — | — |
| `/api/1/devices/{id}/setDateTime` | — | Set | — | — |
| `/api/1/devices/{id}/setNetMode` | — | Set | — | — |
| `/api/1/devices/{id}/startOTA` | — | Start | — | — |
| `/api/1/devices/{id}/snapshot` | — | Create | — | — |
| `/api/1/devices/{id}/endpoints/` | List | — | — | — |
| `/api/1/devices/{id}/endpoints/{epId}` | Get | — | Update | Delete |
| `/api/1/devices/{id}/endpoints/{epId}/reboot` | — | Reboot | — | — |
| `/api/1/devices/{id}/endpoints/{epId}/rmk` | — | RMK | — | — |
| `/api/1/devices/{id}/endpoints/{epId}/call` | — | Call | — | — |
| `/api/1/devices/{id}/interfaces/` | List | — | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}` | Get | — | Update | — |
| `/api/1/devices/{id}/interfaces/{hwIdx}/ports/` | List | — | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}` | — | — | Update | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}/join` | — | Join | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}/leave` | — | Leave | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}/nulling` | Status | Start | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}/gpo` | — | Set | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}/calls/` | List | Call | — | — |
| `/api/1/devices/{id}/interfaces/{ifId}/ports/{pId}/calls/{cId}` | — | — | — | Hangup |
| `/api/1/devices/0/gpio` | List | — | — | — |
| `/api/1/devices/{id}/gpi/{gId}` | — | — | Update | — |
| `/api/1/devices/{id}/gpi/{gId}/addEvent` | — | Add | — | — |
| `/api/1/devices/{id}/gpi/{gId}/events/{eId}` | — | — | Update | Delete |
| `/api/1/devices/{id}/gpo/{gId}` | — | — | Update | — |
| `/api/1/devices/{id}/gpo/{gId}/addEvent` | — | Add | — | — |
| `/api/1/devices/{id}/gpo/{gId}/events/{eId}` | — | — | Update | Delete |
| `/api/1/connections/` | List | Create | — | — |
| `/api/1/connections/{id}` | Get | — | Update | Delete |
| `/api/1/connections/liveStatus` | Live | — | — | — |
| `/api/1/roles/` | List | Create | — | — |
| `/api/1/roles/{id}` | Get | — | Update | Delete |
| `/api/1/events/{entityId}` | Events | — | — | — |
| `/api/1/events/export/{entityId}` | Export | — | — | — |
| `/api/1/externalDevices/` | List | Create | — | — |
| `/api/1/externalDevices/{id}` | Get | — | Update | Delete |
| `/api/1/externalDevices/{id}/ports/{pId}` | — | Add | Update | Delete |
| `/api/1/ivpusers/` | List | Create | — | — |
| `/api/1/ivpusers/{id}` | Get | — | Update | Delete |
| `/api/1/users/` | List | — | — | — |
| `/api/1/users/{username}` | Get | — | Update | — |
| `/api/1/capabilities/linkgroup` | Caps | — | — | — |
| `/api/1/capabilities/interfaces/{type}` | Caps | — | — | — |
| `/api/1/capabilities/devices/{type}` | Caps | — | — | — |
| `/api/1/devices/{id}/license/context` | Download | — | — | — |
| `/api/1/devices/{id}/license/upload` | — | Upload | — | — |

### API v2

| Endpoint | GET | POST |
|----------|-----|------|
| `/api/2/devices/` | List | — |
| `/api/2/devices/{id}` | Get | — |
| `/api/2/devices/{id}/setupnetwork` | — | Configure |
| `/api/2/devices/restore` | — | Restore |
