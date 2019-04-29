import struct




class DNSPacket():
    def unpack(self,data):
        transaction_id = struct.unpack("!H",data[0:2])


    def pack(data):
        pass
