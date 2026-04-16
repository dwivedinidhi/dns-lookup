import dns.reversename
import dns.resolver
from .utils import console, print_error

def run(ip: str):
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
