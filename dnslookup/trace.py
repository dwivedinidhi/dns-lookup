import dns.message
import dns.query
import dns.rdatatype
from .utils import ROOT_SERVERS, console, print_error

def run(domain: str, record_type: str = "A"):
    """Perform iterative DNS trace and show each step."""
    console.print(f"[bold]Tracing [cyan]{domain}[/] ({record_type}) from root servers...[/]\n")

    nameservers = ROOT_SERVERS.copy()
    qname = dns.name.from_text(domain)
    rdtype = dns.rdatatype.from_text(record_type)

    while True:
        for ns in nameservers:
            try:
                query = dns.message.make_query(qname, rdtype)
                response = dns.query.udp(query, ns, timeout=3)

                # Print current server and response status
                status = "Answer" if response.answer else "Referral"
                console.print(f"Querying [yellow]{ns}[/] → [blue]{status}[/]")

                if response.answer:
                    # Print answer records
                    for rrset in response.answer:
                        console.print(f"  [green]{rrset}[/]")
                    console.print()
                    return

                # Check for referral (authority + additional)
                if response.authority and response.additional:
                    # Extract glue records
                    new_ns = []
                    for rrset in response.additional:
                        for rr in rrset:
                            if rr.rdtype == dns.rdatatype.A:
                                new_ns.append(str(rr))
                    if new_ns:
                        console.print(f"  → Next nameservers: {', '.join(new_ns)}\n")
                        nameservers = new_ns
                        break  # continue with new nameservers
                else:
                    # No referral, try next root server
                    continue
            except Exception as e:
                console.print(f"  [red]Error querying {ns}: {e}[/]")
                continue
        else:
            print_error("Trace failed: no further nameservers found.")
            return
