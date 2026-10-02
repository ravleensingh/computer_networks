# Computer Networks Project

## Team Setup (Type 2 — 3 Macs with combined roles)

| Our Mac | Instructor Role(s)         | Services                                                        |
|---------|----------------------------|-----------------------------------------------------------------|
| Mac1    | Mac1 + Mac4 (combined)     | dnsmasq (DNS) · dig · curl · Wireshark · Backend B (port 3002) |
| Mac2    | Mac2                       | nginx (reverse proxy) · TLS certificate · load balancer         |
| Mac3    | Mac3                       | Backend A (port 3001)                                           |

## Architecture

```
Client (Mac1)
  │
  ├─ DNS query (UDP :53) ──► Mac1 dnsmasq
  │   └─ Response: app.teamX.test → Mac2 IP
  │
  └─ HTTPS (TCP :8443) ──► Mac2 nginx (TLS termination)
        ├──► Mac3:3001 (Backend A)  ──► round-robin
        └──► Mac1:3002 (Backend B)  ──► load balancing
```

## How to Run the Backends

### Backend A (Mac3)
```bash
cd backend-a/   # or ~/CN-Project/backend-a/
python3 server.py A 3001
```

### Backend B (Mac1)
```bash
cd backend-b/   # or ~/CN-Project/backend-b/
python3 server.py B 3002
```

Both backends use the **identical** `server.py` code. The only difference is the startup arguments (`A 3001` vs `B 3002`).

### Endpoints

| Endpoint        | Response                                              |
|-----------------|-------------------------------------------------------|
| `GET /`         | JSON confirming service is running                    |
| `GET /api/status` | `{"backend": "A/B", "status": "ok"}` + `X-Backend` header |
| `GET /api/cache`  | Cache-Control + ETag headers; supports 304 Not Modified |

## Team Members

_(Add your names and enrollment numbers here)_

```
XXXXXX Name1
XXXXXX Name2
XXXXXX Name3
```

## Project Structure

```
├── README.md
├── backend-b/
│   └── server.py          # Backend B — runs on Mac1 port 3002
├── dns/
│   └── dnsmasq.conf       # DNS server config (template)
├── evidence/               # Screenshots and captures (not pushed)
└── .gitignore
```

> **Note:** Backend A (`backend-a/`) will be added by Mac3. The nginx config and TLS setup will be added by Mac2.
