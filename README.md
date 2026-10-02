# Computer Networks Project

## Team Setup (Type 2 — 3 Macs with combined roles)

| Our Mac | Instructor Role(s)         | Services                                                        |
|---------|----------------------------|-----------------------------------------------------------------|
| Mac1    | Mac1 + Mac4 (combined)     | dnsmasq (DNS) · dig · curl · Wireshark · Backend B (port 3002) |
| Mac2    | Mac2                       | nginx (reverse proxy) · TLS certificate · load balancer         |
| Mac3    | Mac3                       | Backend A (port 3001)                                           |

## Team Members

_(Add your names and enrollment numbers here)_

```
XXXXXX Name1
XXXXXX Name2
XXXXXX Name3
```

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

## How to Run

### Backend A (Mac3)
```bash
cd backend-a/
python3 server.py A 3001
```

### Backend B (Mac1)
```bash
cd backend-b/
python3 server.py B 3002
```

Both backends use the **identical** `server.py` code. The only difference is the startup arguments (`A 3001` vs `B 3002`).

### Edge / Reverse Proxy (Mac2)

#### Quick Setup
```bash
# From the repo root, run:
cd nginx/
./setup_mac2.sh <Mac1_IP> <Mac3_IP>
```

#### Manual Setup
1. Generate the TLS certificate:
   ```bash
   cd tls/
   ./generate_cert.sh
   ```

2. Deploy nginx config (replace `<Mac1_IP>` and `<Mac3_IP>` with actual IPs):
   ```bash
   # Back up original nginx config
   cp "$(brew --prefix)/etc/nginx/nginx.conf" ~/CN-Project/nginx/nginx.conf.backup

   # Copy TLS files to local project directory
   mkdir -p ~/CN-Project/tls
   cp tls/app.teamX.test.crt ~/CN-Project/tls/
   cp tls/app.teamX.test.key ~/CN-Project/tls/
   chmod 600 ~/CN-Project/tls/app.teamX.test.key

   # Edit nginx/nginx.conf — replace <Mac1_IP>, <Mac3_IP>, <YOUR_USERNAME>
   # Then copy to nginx's config directory
   sudo cp nginx/nginx.conf "$(brew --prefix)/etc/nginx/nginx.conf"

   # Verify and start
   nginx -t
   brew services start nginx
   ```

3. Trust the certificate on Mac2:
   ```bash
   sudo security add-trusted-cert -d -r trustRoot \
     -k /Library/Keychains/System.keychain \
     ~/CN-Project/tls/app.teamX.test.crt
   ```

4. Distribute the `.crt` file to Mac1 and Mac3 (via scp or AirDrop).

### Endpoints

| Endpoint        | Response                                              |
|-----------------|-------------------------------------------------------|
| `GET /`         | JSON confirming service is running                    |
| `GET /api/status` | `{"backend": "A/B", "status": "ok"}` + `X-Backend` header |
| `GET /api/cache`  | Cache-Control + ETag headers; supports 304 Not Modified |

### Testing

```bash
# Verify HTTPS (no -k flag!)
curl -v https://app.teamX.test:8443/api/status

# Load balancing test (should alternate A/B)
for i in {1..6}; do curl -s https://app.teamX.test:8443/api/status; echo; done

# Caching test
curl -i https://app.teamX.test:8443/api/cache

# 304 Not Modified test
curl -i -H 'If-None-Match: "cache-v1"' https://app.teamX.test:8443/api/cache
```

## Project Structure

```
├── README.md
├── backend-b/
│   └── server.py              # Backend B — runs on Mac1 port 3002
├── dns/
│   └── dnsmasq.conf           # DNS server config (template — Mac1)
├── tls/
│   ├── openssl.cnf            # OpenSSL config for cert generation
│   ├── generate_cert.sh       # Script to generate self-signed TLS cert
│   ├── app.teamX.test.crt     # Self-signed certificate (generated, not tracked)
│   └── app.teamX.test.key     # Private key (NEVER leaves Mac2, not tracked)
├── nginx/
│   ├── nginx.conf             # nginx reverse proxy config (template)
│   └── setup_mac2.sh          # Automated Mac2 deployment script
├── evidence/                   # Screenshots and captures (not pushed)
└── .gitignore
```

> **Note:** Backend A (`backend-a/`) will be added by Mac3. The `backend-b/server.py` code is identical — Mac3 copies it to `backend-a/`.
