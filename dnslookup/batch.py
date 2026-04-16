import concurrent.futures
from .query import run as query_run
from .utils import console, print_error

def run(file_path: str, record_types: list = None):
    try:
        with open(file_path, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print_error(f"File '{file_path}' not found.")
        return

    if not domains:
        print_error("No domains found in file.")
        return

    console.print(f"[bold]Processing {len(domains)} domains...[/]\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(query_run, domain, record_types): domain for domain in domains}
        for future in concurrent.futures.as_completed(futures):
            domain = futures[future]
            try:
                future.result()
            except Exception as e:
                print_error(f"Failed for {domain}: {e}")
