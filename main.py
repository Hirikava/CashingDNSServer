import  asyncio
import argparse
import sys

from dns_network import DNSProtocol,DNSTransport
from dns_cashe import DNSCashe


parser = argparse.ArgumentParser()
parser.add_argument("-dns",type=str,help="Addres of remote dns server")
parser.add_argument("-ud",type=int,help="Cashe Update Interval")
parser.add_argument("--load", type=str,help="File of pickled cashe")
parser.add_argument("--store", type=str, help="File to store cashe")

args = parser.parse_args(sys.argv[1:])
if(args.dns):
    DNSProtocol((args.dns,53))
if(args.ud):
    DNSCashe().set_ud(args.ud)
if(args.load):
    DNSCashe().set_cashe(args.load)

loop  = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(protocol_factory=DNSProtocol(),sock = DNSTransport().socket)
transport,proto = loop.run_until_complete(coro)
proto.set_transport(transport)
wait_tasks =  asyncio.wait([loop.create_task(coro),loop.create_task(DNSCashe().save_cashe(args.store)),loop.create_task(DNSCashe().update_cashe())])
loop.run_until_complete(wait_tasks)

