import struct


TYPE_A = 1
TYPE_AAAA = None
TYPE_NS = None
TYPE_PTR = None

class Querry():
    def __init__(self,domen,querry_type,querry_class):
        self.domen = domen
        self.querry_type = querry_type
        self.querry_class = querry_class

    @classmethod
    def unpack(cls,data):
        pass

    def pack(self):
        pass

class Headers():
    def __init__(self,transaction_id,questions,answer_RRs,authority_RRs,additional_RRs,flags = 256):
        self.transaction_id =transaction_id
        self.questions = questions
        self.answer_RRs = answer_RRs
        self.authority_RRs = authority_RRs
        self.additional_RRs = additional_RRs
        self.flags = flags

    @classmethod
    def unpack(cls,data):
        unpacked_data = struct.unpack("!HHHHHH",data)
        transaction_id = unpacked_data[0]
        flags = unpacked_data[1]
        questions = unpacked_data[2]
        answer_RRs = unpacked_data[3]
        authority_RRs = unpacked_data[4]
        additional_RRs = unpacked_data[5]
        return Headers(transaction_id,questions,answer_RRs,authority_RRs,additional_RRs,flags)

    def pack(self):
        pass

    def __str__(self):
        return str.format("Transactions id:{0}\nFlags:{1}\nQuestions:{2}\nAnswerRRs:{3}\nAuthorityRRs:{4}\nAdditionalRRs:{5}\n"
                             ,self.transaction_id,self.flags,self.questions,self.answer_RRs,self.authority_RRs,self.additional_RRs)





class DNSRequest():
    def unpack(self,data):
        headers = Headers.unpack(data[0:12])
        print(headers)
        print(data[12:])
        self.read_querry(data[12:])

    def pack(self,querres):
        pass

    def read_querry(self,data):
        final_domen_name = b''
        dot_flag = False
        while(data[0:1] != b'\x00'):
            lenght_byte = data[0:1]
            length = struct.unpack("!B",lenght_byte)[0]
            domen_name = struct.unpack("!" + ("c" * length),data[1:1+length])
            if(dot_flag):
                final_domen_name += (b'.')
            final_domen_name +=  (b'').join(domen_name)
            data = data[1+length:]
            dot_flag = True
        data = data[1:]
        querry_type = struct.unpack("!H",data[0:2])[0]
        querry_class = struct.unpack("!H",data[2:4])[0]
        print(str.format("Domen:{0}\nQuerry Type:{1}\nQuerry Class:{2}",final_domen_name,querry_type,querry_class))

