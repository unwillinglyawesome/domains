import ipaddress
from pprint import pprint
from urllib.request import urlopen, Request


def get_digital_ocean_ips() -> list[ipaddress.IPv4Network]:
    url = "https://www.digitalocean.com/geo/google.csv"

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as r:
        text = r.read().decode('utf-8')

    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        part = line.split(',', 1)[0].strip()
        if ':' in part:
            continue
        try:
            net = ipaddress.ip_network(part, strict=False)
            if isinstance(net, ipaddress.IPv4Network):
                result.append(net)
        except ValueError:
            pass
    return result

def get_cloudflare_ips() -> list[ipaddress.IPv4Network]:
    url = "https://www.cloudflare.com/ips-v4/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as r:
        text = r.read().decode('utf-8')

    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
            if isinstance(net, ipaddress.IPv4Network):
                result.append(net)
        except ValueError:
            pass
    return result

def get_telegram_ips() -> list[ipaddress.IPv4Network]:
    url = "https://core.telegram.org/resources/cidr.txt"
    with urlopen(url) as r:
        text = r.read().decode('utf-8')

    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
            if isinstance(net, ipaddress.IPv4Network):
                result.append(net)
        except ValueError:
            pass
    return result

subnets = sorted(
    get_digital_ocean_ips() +
    get_cloudflare_ips() +
    get_telegram_ips(),
    key=lambda net: net.network_address
)

with open('lists/ips.lst', 'w', encoding='utf-8', newline='\n') as file:
    for subnet in subnets:
        file.write(str(subnet) + '\n')