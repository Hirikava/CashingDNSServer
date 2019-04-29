from socket import *
from dns_packets import DNSRequest

udp_socket = socket(AF_INET,SOCK_DGRAM)
udp_socket.bind(('localhost',53))
data = udp_socket.recv(1024)
DNSRequest().unpack(data)