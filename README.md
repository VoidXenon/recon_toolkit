# recon_toolkit
Recon Toolkit is a professional, all-in-one reconnaissance utility for Kali Linux. It supports multiple modes of operation:

- **OSINT**: Gather public data about an email address (Gravatar, MX records, common social platforms).
- **NET**: Scan a target IP address for open ports on common services.
- **SYS**: Collect local system information useful for privilege escalation and auditing.

---

## Features
- Passive OSINT gathering (email and social footprints)
- Common TCP port scanner
- Gravatar profile checker
- MX record lookup using DNS
- Local system enumeration (users, sudoers, worl-writable files)
- CLean JSON output

---

## Requirements

- Python 3.x
- Kali Linux or any Linux distro
- 'pip3 install dnspython requests'

---

## Usage


### OSINT Mode

```bash
python3 recon_toolkit.py osint -t someone@example.com
```

### Network Scan Mode

```bash
python3 recon_toolkit.py osint -t "IP"
```

### System Info Mode
```bash
python3 recon_toolkit.py osint -t sys
```

---

## Disclaimer
This tool is for **educational** and **authorized security testing** purposes only. Unauthorized use is prohibited.

---

## License

MIT License
