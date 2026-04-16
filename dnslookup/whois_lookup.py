import whois
from .utils import console, print_error

def run(domain: str):
    """Fetch and display WHOIS information."""
    try:
        w = whois.whois(domain)
        console.print(f"[bold]WHOIS for [cyan]{domain}[/][/]\n")
        for key, value in w.items():
            if value:
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                console.print(f"[green]{key}:[/] {value}")
    except Exception as e:
        print_error(f"WHOIS lookup failed: {e}")
