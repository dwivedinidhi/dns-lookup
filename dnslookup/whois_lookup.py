import whois
from .utils import console, print_error

def run(domain: str):
    try:
        # Try python-whois style (whois.whois)
        if hasattr(whois, 'whois'):
            w = whois.whois(domain)
        # Fallback to whois.query style
        elif hasattr(whois, 'query'):
            w = whois.query(domain)
        else:
            raise ImportError("Unsupported whois library. Install 'python-whois'.")
        
        console.print(f"[bold]WHOIS for [cyan]{domain}[/][/]\n")
        for key, value in w.items():
            if value:
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                console.print(f"[green]{key}:[/] {value}")
    except Exception as e:
        print_error(f"WHOIS lookup failed: {e}")
