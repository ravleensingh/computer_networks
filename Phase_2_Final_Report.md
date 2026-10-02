# Computer Networks Project - Phase 2 Final Report

## Changes from Phase 1
- **Extension A (Backup DNS Resolver)**: A secondary `dnsmasq` instance was configured on Mac 3 to serve as a backup DNS. Clients were updated to use both Mac 1 and Mac 3 as their DNS servers. This provided resilience against the failure of the primary DNS server.
- **Extension B (DNS TTL & Controlled Change)**: DNS TTLs were lowered to demonstrate controlled caching behavior. We updated `dnsmasq.conf` to observe how clients cache IP resolutions and how a DNS cutover behaves in real time when TTL expires.
- **Extension C (Service Isolation)**: `pf` firewall rules were implemented on Mac 3 to isolate Backend A. Direct connections from clients to Port 3001 were blocked, ensuring all traffic originates exclusively from the Edge Load Balancer (Mac 2), satisfying security requirements.
- **Extension D (High-Availability Failover)**: Nginx upstream configuration was enhanced with `max_fails` and `fail_timeout` parameters. This allowed the edge proxy to gracefully route around stopped backend nodes instead of blindly sending traffic and returning 502 Bad Gateway.
- **Extension E (DNS-Based Edge Cutover)**: We set up a standby nginx server on Mac 3. The `app.teamX.test` DNS record was temporarily updated to point to Mac 3's IP to showcase DNS-based disaster recovery of the edge layer itself without new hardware.

## Resilience Tests and Results
1. **Application Server Failure**: Shutting down Backend A correctly caused nginx to detect the failure (Extension D) and forward all traffic to Backend B without client-facing errors.
2. **DNS Server Failure**: Shutting down Mac 1's dnsmasq server seamlessly allowed clients to resolve names using Mac 3's dnsmasq instance (Extension A), proving high availability for name resolution.

## Troubleshooting Findings (Extension F)
During the troubleshooting challenge, we employed a systematic approach. First, `dig` was used to ensure DNS resolved to the correct Edge IP. Second, `nc -vz` confirmed TCP connectivity to the required port. Finally, `curl -v` helped verify the TLS handshake and HTTP response. We found that isolating the layers (DNS -> Network -> Application) was critical for rapid diagnosis.

## Learning Summaries
- **Extension A (Backup DNS)**: We learned how client operating systems utilize primary and secondary DNS resolvers, recognizing that application-level failures (Backend downtime) and infrastructure-level failures (DNS downtime) require distinct architectural mitigations.
- **Extension B (DNS TTL)**: Modifying DNS TTL demonstrated the inherent trade-off between aggressive caching (which reduces DNS server load and latency) and agility (the ability to rapidly migrate clients to new IP addresses).
- **Extension C (Firewall Isolation)**: Utilizing macOS `pf` rules revealed how critical network-level segmentation is for a defense-in-depth strategy, preventing clients from bypassing the reverse proxy and hitting backend endpoints directly.
- **Extension D (HA Failover)**: We saw firsthand how load balancers mask backend volatility from end users. By tweaking `max_fails`, nginx successfully insulated the client from a simulated server crash.
- **Extension E (Edge Cutover)**: Migrating the reverse proxy via DNS highlighted how DNS can be leveraged as a global routing mechanism for disaster recovery, bypassing the need for identical localized hardware failover mechanisms.
- **Extension F (Troubleshooting)**: The hands-on challenge crystallized the importance of the OSI model; effectively debugging issues means starting at Layer 3/4 (IP/TCP) before assuming an application bug (Layer 7).
