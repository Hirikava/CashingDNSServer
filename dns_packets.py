import struct

DNS_TYPE_A = 1
DNS_TYPE_AAAA = 28
DNS_TYPE_PTR = 12
DNS_TYPE_CNAME = 5
DNS_TYPE_MX = 15
DNS_TYPE_NS = 2

DNS_CLASS_IN = 1
DNS_CLASS_OUT = None


class DNSPacketParser():
    def __init__(self,headers,querry,answer):
        self.headers = headers
        self.querry = querry
        self.answer = answer

    @classmethod
    def unpack(cls,data):
        headers = DNSPacketParser.__unpack_headers(data)
        querryes = []
        answers = []
        offset = 12
        for i in range(0,headers.questions):
            result = DNSPacketParser.__unpack_question(data[offset:])
            querryes.append(result[0])
            offset += result[1]

        for i in range(0,headers.answer_rrs):
            result = DNSPacketParser.__unpack_answer(data[offset:])
            result[0].name = querryes[0].name
            answers.append(result[0])
            offset+= result[1]
        return headers,querryes[0],answers


    @classmethod
    def __unpack_headers(cls,data):
        transaction_id,flags,questions,anwer_rrs,authority_rrs,additional_rrs =  struct.unpack("!HHHHHH",data[0:12])
        return DNSHeaders(transaction_id,flags,questions,anwer_rrs,authority_rrs,additional_rrs)

    @classmethod
    def __unpack_question(cls,data):
        first_querry_flag = True
        final_domen_name = b''
        offset = 0
        cdata = data[0:]
        while(struct.unpack("!b",data[0:1])[0] != 0):
            length = struct.unpack('!b',data[0:1])[0]
            if(not first_querry_flag):
                final_domen_name += b'.'
            final_domen_name += data[1:length+1]
            data = data[length+1:]
            offset += length + 1
            first_querry_flag = 0
        querry_type,class_type = struct.unpack("!HH",data[1:5])
        offset += 5
        return DNSQuerry(cdata[0:offset],final_domen_name,querry_type,class_type),offset

    @classmethod
    def __unpack_answer(cls,data):
        typee,cls,ttl,data_length = struct.unpack("!HHLH",data[2:12])
        raw_data = data[12:12+data_length]
        return DNSAnswer(name=None,type=typee,cls=cls,ttl=ttl,length=data_length,data=raw_data), 12+data_length


class DNSHeaders():
    def __init__(self,transaction_id,flags,questions,answer_rrs,authority_rrs,additional_rrs):
        self.transaction_id = transaction_id
        self.flags = flags
        self.questions = questions
        self.answer_rrs = answer_rrs
        self.authority_rrs = authority_rrs
        self.additional_rrs = additional_rrs

    def __str__(self):
        return str.format("Transaction id:{0}\nFlags:{1}\nQuestions:{2}\nAnswer RRs:{3}\nAuthority RRs:{4}\nAdditional RRs:{5}"
                          ,self.transaction_id,self.flags,self.questions,self.answer_rrs,self.authority_rrs,self.additional_rrs)

    def pack(self):
        return struct.pack("!HHHHHH",self.transaction_id,self.flags,self.questions,self.answer_rrs,self.authority_rrs,self.additional_rrs)

class DNSQuerry():
    def __init__(self,raw_data,name,type,class_type):
        self.raw_data = raw_data
        self.name = name
        self.type = type
        self.class_type = class_type

    def __str__(self):
        return str.format("Name:{0}\nType:{1}\nClass:{2}",self.name,self.type,self.class_type)

    def pack(self):
        return


class DNSAnswer():
    def __init__(self,name,type,cls,ttl,length,data):
        self.name = name
        self.cls = cls
        self.type = type
        self.ttl = ttl
        self.lenght = length
        self.data = data

    def pack(self):
        return b'\xc0\x0c' + struct.pack("!HHLH",self.type,self.ttl,self.cls,self.lenght) + self.data

    def __str__(self):
        return str.format("Name:{0}\nType:{1}\nClass:{2}\nTTL:{3}\nData:{4}\n",self.name,self.type,self.cls,self.ttl,self.data)

