import dns.resolver
from rich.table import Table
from .utils import console, print_error

def run(domain: str, record_types: list = None):
    if record_types is None:
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA"]

    table = Table(title=f"DNS Records for [bold cyan]{domain}[/]")
    table.add_column("Type", style="green")
    table.add_column("TTL", style="yellow")
    table.add_column("Value", style="white")

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for ans in answers:
                ttl = getattr(ans, 'ttl', 'N/A')
                # Format value for readability
                value = str(ans)
                if rtype == "MX":
                    value = f"{ans.preference} {ans.exchange}"
                elif rtype == "SOA":
                    value = f"{ans.mname} {ans.rname} ({ans.serial}, {ans.refresh}, {ans.retry}, {ans.expire}, {ans.minimum})"
                table.add_row(rtype, str(ttl), value)
        except dns.resolver.NoAnswer:
            table.add_row(rtype, "-", "[dim]No records[/]")
        except dns.resolver.NXDOMAIN:
            print_error(f"Domain '{domain}' does not exist.")
            return
        except dns.exception.Timeout:
            print_error(f"Timeout querying {rtype} records.")
        except Exception as e:
            table.add_row(rtype, "-", f"[red]Error: {e}[/]")

    console.print(table)
