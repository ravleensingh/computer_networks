# CN Project — Final Test Results
# Date: 2026-10-03
# Tested from: Mac3 (Shitanshu, 10.7.7.23) as client
# Reason: Mac1 has Heimdall VPN proxy blocking outbound TCP connections

## Network Configuration
| Machine | IP | Role |
|---------|-----|------|
| Mac1 (Ravleen) | 10.7.20.106 | DNS Server (dnsmasq) + Backend B (:3002) |
| Mac2 (Lakshay) | 10.7.19.222 | Nginx Edge + TLS Termination (:8443) |
| Mac3 (Shitanshu) | 10.7.7.23 | Backend A (:3001) + Test Client |

## TEST 1: DNS Resolution ✅
dig app.teamX.test → 10.7.19.222
SERVER: 10.7.20.106#53 (Mac1 dnsmasq)
dig @8.8.8.8 app.teamX.test → (empty / NXDOMAIN) — domain is private

## TEST 2: HTTPS ✅
curl -v https://app.teamX.test:8443/api/status
- TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256
- subjectAltName: host "app.teamX.test" matched cert's "app.teamX.test"
- SSL certificate verify ok (no -k flag needed)
- HTTP/1.1 200 OK
- X-Backend: A

## TEST 3: Load Balancing ✅ (Perfect round-robin)
Request 1: {"backend": "B"}
Request 2: {"backend": "A"}
Request 3: {"backend": "B"}
Request 4: {"backend": "A"}
Request 5: {"backend": "B"}
Request 6: {"backend": "A"}
Request 7: {"backend": "B"}
Request 8: {"backend": "A"}
Request 9: {"backend": "B"}
Request 10: {"backend": "A"}

## TEST 4: HTTP Caching ✅
HTTP/1.1 200 OK
Cache-Control: max-age=60
ETag: "cache-v1"
{"backend": "B", "cached": true}

## TEST 5: 304 Not Modified ✅
HTTP/1.1 304 Not Modified
Cache-Control: max-age=60
ETag: "cache-v1"
(empty body — correct!)
