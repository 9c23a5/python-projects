# This is meant to be ran as a cronjob
# Compare the IP from domain with the router reported IP and update domain as needed

import asyncio
from sagemcom_api.enums import EncryptionMethod
from sagemcom_api.client import SagemcomClient
import secrets # Our secrets.py file
import requests

DOMAIN = "vpn.xn--ts9haa.ws"

INTERNAL_IP = "192.168.1.1"
ROUTER_USER = "1234"
ROUTER_PASS = "1234"

CF_HEADERS = {
    "Authorization" : f"Bearer {secrets.CF_API}",
    "Content-Type" : "application/json"
}

# Verify API
#resp = requests.get("https://api.cloudflare.com/client/v4/user/tokens/verify", headers=CF_HEADERS)

# List all DNS Records
resp = requests.get(f"https://api.cloudflare.com/client/v4/zones/{secrets.CF_ZONE}/dns_records", headers=CF_HEADERS)

dns_records = resp.json()
for record in dns_records['result']:
    if record['name'] == DOMAIN:
        CF_IP = record['content']
        CF_ID = record['id']
        break

print(f"IP for {DOMAIN} is {CF_IP}")

async def main() -> None:
    async with SagemcomClient(INTERNAL_IP, ROUTER_USER, ROUTER_PASS, EncryptionMethod.MD5) as gw_client:

        # Login
        try:
            await gw_client.login()
        except Exception as exception:
            print(exception)
            return

        try:
            # Get all interfaces
            result = await gw_client.get_value_by_xpath("Device/IP/Interfaces")
            for iface in result:
                # Get our internet facing inerface and return its IP
                if iface["alias"] == "IP_DATA":
                    PUBLIC_IP = iface["i_pv4_addresses"][0]["ip_address"]
                    return PUBLIC_IP

        except Exception as exception:
            print(exception)

#router_info, result = asyncio.run(main())
PUBLIC_IP = asyncio.run(main())

#print(router_info)
print(f"Our public IP is {PUBLIC_IP}")

if CF_IP != PUBLIC_IP:
    print("Updating DNS Records...")

    # Add Public IP to domain
    new_dns = {
        "content" : PUBLIC_IP,
        "name" : DOMAIN,
        "proxied" : True,
        "ttl" : 1
    }

    patch_dns = requests.patch(f"https://api.cloudflare.com/client/v4/zones/{secrets.CF_ZONE}/dns_records/{CF_ID}", json=new_dns, headers=CF_HEADERS)

    print(f"{patch_dns.status_code=}")
    print(patch_dns.json())

else:
    print("No update needed")