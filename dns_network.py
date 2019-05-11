import asyncio
import socket
from singletone import singleton
import dns_packets
from dns_packets import DNSPacketParser
from dns_transaction_meneger import DNSTransactionManager
from dns_cashe import DNSCashe

@singleton
class DNSProtocol(asyncio.DatagramProtocol):
    def __init__(self,remote_dns_addres = ('10.74.240.10',53)):
        asyncio.DatagramProtocol.__init__(self)
        self.remote_dns = remote_dns_addres

    def __call__(self, *args, **kwargs):
        return self

    def error_received(self, exc):
        print("sosamba")

    def datagram_received(self, data, addr):
        headers,querry,answers = DNSPacketParser.unpack(data)


        for answer in answers:
            DNSCashe().push_to_cash(answer)

        result_addr = DNSTransactionManager().check_transaction(transaction_id=headers.transaction_id,addres=addr)
        if(result_addr):
            self.transport.sendto(data, result_addr)

        if(headers.answer_rrs == 0 and headers.authority_rrs == 0 and headers.authority_rrs == 0):
            result_record = DNSCashe().get_record(querry.type,querry.name)
            if(result_record):
                if(result_record.type == dns_packets.DNS_TYPE_A or result_record.type == dns_packets.DNS_TYPE_AAAA):
                    headers.answer_rrs = 1
                else:
                    headers.authority_rrs = 1
                self.transport.sendto(headers.pack() + querry.raw_data + result_record.pack(),DNSTransactionManager().check_transaction(headers.transaction_id,addr))
            else:
                self.transport.sendto(data,self.remote_dns)



    def set_transport(self,transport):
        self.transport = transport



@singleton
class DNSTransport(asyncio.DatagramTransport):
    def __init__(self,local_addres = ('',53)):
        asyncio.DatagramTransport.__init__(self)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(local_addres)











