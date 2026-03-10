# FreeSpeak II Base Station API

Unofficial REST API documentation for the Clear-Com FreeSpeak II base station.

The FreeSpeak II base station runs an Express.js web server with a full JSON REST API and Socket.IO real-time events. This API is used internally by the CCM (Clear-Com Configuration Manager) web interface but is not publicly documented by Clear-Com. This project aims to document the API for interoperability and integration purposes.

> **Disclaimer:** This project is not affiliated with, endorsed by, or connected to Clear-Com in any way. All product names, trademarks, and registered trademarks are the property of their respective owners. This documentation was created through observation of the CCM web interface for interoperability purposes. Use at your own risk.

## Quick Start

The base station uses **HTTP Digest authentication**. All API responses are JSON.

```bash
# List all devices
curl --digest -u USERNAME:PASSWORD http://BASE_STATION_IP/api/1/devices/

# Get antenna and beltpack status
curl --digest -u USERNAME:PASSWORD http://BASE_STATION_IP/api/1/devices/1/endpoints/

# Get live partyline status (who's talking)
curl --digest -u USERNAME:PASSWORD http://BASE_STATION_IP/api/1/connections/liveStatus

# Get all roles
curl --digest -u USERNAME:PASSWORD http://BASE_STATION_IP/api/1/roles/
```

## What You Can Do

**Read-only monitoring (GET requests):**
- See which antennas/transceivers are online or offline
- Monitor beltpack battery levels, signal strength (RSSI), and link quality
- See who is talking/listening on which partyline in real time
- View all role configurations and connection assignments
- Check device health, alerts, and firmware versions
- Monitor GPIO states

**Configuration (PUT/POST requests):**
- Update role settings (keyset assignments, audio levels, alert modes)
- Rename connections, ports, and endpoints
- Associate ports with partylines
- Manage GPIO event triggers
- Backup and restore configurations

**Real-time events (Socket.IO):**
- Subscribe to live endpoint updates (beltpack status changes)
- Monitor connection activity in real time
- Receive GPIO state change notifications
- Track device and interface status

## Documentation

- **[API Reference](docs/api-reference.md)** — Complete endpoint documentation with request/response examples
- **[Interactive Reference](https://paulfehr90.github.io/freespeak-ii-api/)** — Browsable HTML reference (via GitHub Pages)
- **[Examples](examples/)** — Python and shell script examples

## API Overview

| Category | Endpoints | Description |
|----------|-----------|-------------|
| [Devices](docs/api-reference.md#devices) | 8 GET, 11 POST, 1 PUT | Base station config, network, firmware, backup/restore |
| [Endpoints](docs/api-reference.md#endpoints-antennas--beltpacks) | 2 GET, 4 POST, 1 PUT, 1 DELETE | Antennas and beltpacks — status, battery, RSSI |
| [Connections](docs/api-reference.md#connections-partylines--groups) | 3 GET, 2 POST, 1 PUT, 1 DELETE | Partylines, groups, live talk/listen status |
| [Roles](docs/api-reference.md#roles) | 2 GET, 1 POST, 1 PUT, 1 DELETE | Beltpack profiles and keyset config |
| [Interfaces](docs/api-reference.md#audio-interfaces) | 2 GET, 1 PUT | Station, 2-wire, and 4-wire interfaces |
| [Ports](docs/api-reference.md#ports) | 2 GET, 4 POST, 1 PUT, 1 DELETE | Port settings, join/leave, nulling, SIP calls |
| [GPIO](docs/api-reference.md#gpio) | 1 GET, 2 POST, 2 PUT, 2 DELETE | General purpose inputs and outputs |
| [Socket.IO](docs/api-reference.md#socketio-real-time-events) | 15 topics | Real-time event streaming |

## Tested On

- FreeSpeak II Base Station
- Firmware: 1.6.15.0
- Hardware: v2-2

Other firmware versions may have different endpoints or behavior. Contributions from users on different versions are welcome.

## Use Cases

- **Bitfocus Companion module** — Build a Companion module for StreamDeck integration
- **Monitoring dashboards** — Battery levels, antenna status, channel activity
- **Automated alerts** — Low battery warnings, antenna offline notifications
- **Show logging** — Record who talked on which channel and when
- **Integration with other systems** — Bridge with OSC, MIDI, or other show control protocols

## Contributing

If you have a FreeSpeak II (or Edge, or other CCM-based system) and discover additional endpoints or behavior differences, please open an issue or pull request.

## License

MIT License — see [LICENSE](LICENSE).
