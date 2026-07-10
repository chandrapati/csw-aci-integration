#!/usr/bin/env python3
"""Create a Cisco ACI connector in Cisco Secure Workload via OpenAPI.

REFERENCE / LEARNING ONLY. The exact request schema and endpoint may vary by
CSW release — always confirm against the CSW OpenAPI documentation for your
version. Prefer configuring the ACI connector in the UI unless you are
automating at scale.

Security (per repo policy):
  * NEVER hardcode APIC credentials or the CSW API key/secret.
  * Read all secrets from environment variables (or a secrets manager) at runtime.
  * Do not commit any file containing real credentials (see ../.gitignore).

Env vars expected:
  CSW_API_ENDPOINT     e.g. https://csw.example.com
  CSW_API_KEY          CSW API key   (capability: external_integration / connectors)
  CSW_API_SECRET       CSW API secret
  APIC_USERNAME        APIC service-account username
  APIC_PASSWORD        APIC service-account password
"""
import os
import json

# The CSW SDK provides a signed REST client (tetpyclient.RestClient). This file
# shows the *payload shape*; wire it to your CSW client of choice.
REQUIRED = ["CSW_API_ENDPOINT", "CSW_API_KEY", "CSW_API_SECRET",
            "APIC_USERNAME", "APIC_PASSWORD"]

missing = [k for k in REQUIRED if not os.environ.get(k)]
if missing:
    raise SystemExit(f"Missing required env vars: {', '.join(missing)}")

aci_connector_payload = {
    "name": "aci-dc1-fabric",
    "type": "aci",
    "description": "DC1 ACI fabric - endpoints + ESG segmentation",
    # Up to 7 APIC nodes. Point at the APIC controllers, not leaf/spine switches.
    "apic_nodes": [
        {"host_name": "10.10.0.11", "port_number": 443},
        {"host_name": "10.10.0.12", "port_number": 443},
        {"host_name": "10.10.0.13", "port_number": 443},
    ],
    # Credentials pulled from env / secrets manager - never inline.
    "username": os.environ["APIC_USERNAME"],
    "password": os.environ["APIC_PASSWORD"],
    "self_signed_cert": True,          # match your APIC certificate
    # Connectivity: direct (no proxy), Secure Connector tunnel, or HTTP proxy.
    "use_secureconnector_tunnel": False,
    # "http_proxy": "http://proxy.example.com:3128",  # ports 80/8080/443/3128
}

print("ACI connector payload (POST to the CSW connectors/ACI endpoint):")
print(json.dumps({**aci_connector_payload, "password": "***REDACTED***"}, indent=2))

# Example (pseudo) — adapt to your CSW REST client:
#
# from tetpyclient import RestClient
# rc = RestClient(os.environ["CSW_API_ENDPOINT"],
#                 api_key=os.environ["CSW_API_KEY"],
#                 api_secret=os.environ["CSW_API_SECRET"],
#                 verify=True)
# resp = rc.post("/connectors/aci", json_body=json.dumps(aci_connector_payload))
# print(resp.status_code, resp.text)
