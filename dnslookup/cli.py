import argparse
from . import query, reverse, trace, batch, whois_lookup

def main():
    parser = argparse.ArgumentParser(
        prog="dnslookup",
        description="Advanced DNS lookup CLI tool with colored table output."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand")

    # query
    parser_query = subparsers.add_parser("query", help="Query DNS records for a domain")
    parser_query.add_argument("domain", help="Domain name to query")
    parser_query.add_argument("-t", "--type", action="append", dest="record_types",
                              help="Record type (can be used multiple times). Default: A,AAAA,MX,NS,TXT,SOA")

    # reverse
    parser_rev = subparsers.add_parser("reverse", help="Reverse DNS lookup (PTR)")
    parser_rev.add_argument("ip", help="IP address to resolve")

    # trace
    parser_trace = subparsers.add_parser("trace", help="Trace DNS resolution path")
    parser_trace.add_argument("domain", help="Domain to trace")
    parser_trace.add_argument("-t", "--type", default="A", help="Record type (default: A)")

    # batch
    parser_batch = subparsers.add_parser("batch", help="Query multiple domains from a file concurrently")
    parser_batch.add_argument("file", help="File containing one domain per line")
    parser_batch.add_argument("-t", "--type", action="append", dest="record_types",
                              help="Record types to query (can be repeated)")

    # whois
    parser_whois = subparsers.add_parser("whois", help="WHOIS lookup for a domain")
    parser_whois.add_argument("domain", help="Domain to lookup")

    args = parser.parse_args()

    if args.command == "query":
        query.run(args.domain, args.record_types)
    elif args.command == "reverse":
        reverse.run(args.ip)
    elif args.command == "trace":
        trace.run(args.domain, args.type)
    elif args.command == "batch":
        batch.run(args.file, args.record_types)
    elif args.command == "whois":
        whois_lookup.run(args.domain)
