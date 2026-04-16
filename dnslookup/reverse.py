import ipaddress
import dns.reversename
import dns.resolver
from .utils import console, print_error

def run(ip: str):
    # Validate IP address
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print_error(f"'{ip}' is not a valid IP address. Reverse lookup requires an IP.")
        return

    try:
        addr = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(addr, "PTR")
        console.print(f"[bold green]Reverse lookup for {ip}:[/]")
        for ans in answers:
            console.print(f"  → {ans.target}")
    except dns.resolver.NXDOMAIN:
        print_error(f"No PTR record found for {ip}")
    except Exception as e:
        print_error(str(e))
