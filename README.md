# CP-ABE-Cloud-EHR-Storage

## Generate JWT key pairs
```bash
openssl genpkey -algorithm Ed25519 -out ed25519key.pem
openssl pkey -in ed25519key.pem -pubout -out ed25519pubkey.pem
```

## HTTPS
- Dùng [Duck DNS](https://www.duckdns.org) tạo hai free DNS record cloud8742.duckdns.org và as8742.duckdns.org.
- Sau đó dùng [SSL For Free](https://www.sslforfree.com/) để ký cert.
