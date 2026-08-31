#! /usr/bin/env bash

set -e
set -x

KEYS_DIR="certificates"
PRIVATE_KEY="$KEYS_DIR/jwt-private.pem"
PUBLIC_KEY="$KEYS_DIR/jwt-public.pem"

mkdir -p "$KEYS_DIR"

# Generate an RSA private key, of size 2048
echo "Generating RSA private key..."
openssl genrsa -out "$PRIVATE_KEY" 2048
chmod 600 "$PRIVATE_KEY"

echo "Generating public key..."
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in "$PRIVATE_KEY" -outform PEM -pubout -out "$PUBLIC_KEY"
chmod 644 "$PUBLIC_KEY"

echo "JWT keys ready:"
echo "  Private: $PRIVATE_KEY"
echo "  Public:  $PUBLIC_KEY"

exec "$@"