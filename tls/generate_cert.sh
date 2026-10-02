#!/bin/bash
# generate_cert.sh — Generate self-signed TLS certificate for CN Project
# Run this script from the tls/ directory on Mac2
#
# Usage: ./generate_cert.sh
# Output: app.teamX.test.key (PRIVATE — stays on Mac2 only!)
#         app.teamX.test.crt (distribute to Mac1 and Mac3)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== CN Project — TLS Certificate Generator ==="
echo ""

# Generate the self-signed certificate
openssl req -x509 -nodes -newkey rsa:2048 -sha256 \
  -days 30 \
  -keyout app.teamX.test.key \
  -out app.teamX.test.crt \
  -config openssl.cnf \
  -extensions req_ext

# Protect the private key
chmod 600 app.teamX.test.key

echo ""
echo "=== Certificate generated successfully ==="
echo ""

# Verify the certificate details
echo "--- Certificate Details ---"
openssl x509 -in app.teamX.test.crt -noout -subject -issuer -dates -ext subjectAltName

echo ""
echo "=== IMPORTANT ==="
echo "1. The private key (app.teamX.test.key) must NEVER leave Mac2."
echo "2. Distribute ONLY app.teamX.test.crt to Mac1 and Mac3:"
echo "   scp app.teamX.test.crt <Mac1_user>@<Mac1_IP>:~/"
echo "   scp app.teamX.test.crt <Mac3_user>@<Mac3_IP>:~/"
echo "3. On Mac1/Mac3: Import the .crt into Keychain Access → login → Always Trust"
echo ""
