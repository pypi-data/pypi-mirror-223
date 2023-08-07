import asyncio
import argparse
import os
from revwhox.whoisxmlapi import whoisxmlapi
from revwhox.viewdns import viewDNS

try:
    # https://reverse-whois.whoisxmlapi.com
    whoisxmlapi_key = os.environ['WHOISXMLAPI']
except Exception:
    pass


async def reverse_whois(company: str) -> None:
    tasks = [whoisxmlapi(company, whoisxmlapi_key), viewDNS(company)]
    domains_sets: list = await asyncio.gather(*tasks)
    domains_list = [list(domains) for domains in domains_sets]
    domains = '\n'.join('\n'.join(domain) for domain in domains_list)
    print(domains)


parser = argparse.ArgumentParser()
parser.add_argument('company', metavar='Organization', help='e.g. "Wal-Mart Stores, Inc."')
args = parser.parse_args()
asyncio.run(reverse_whois(args.company))
