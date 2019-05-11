from singletone import singleton
import pickle
import asyncio

@singleton
class DNSCashe():
    def __init__(self):
        self.cashe = dict()
        self.upd_freq = 5

    def set_ud(self,val):
        self.upd_freq = val

    def push_to_cash(self,answer):
        self.cashe[(answer.name,answer.type)] = [answer,answer.ttl]

    def get_record(self,type,name):
        if (name,type) in self.cashe.keys():
            ret_record = self.cashe[(name,type)][0]
            ret_record.ttl = self.cashe[(name,type)][1]
            return ret_record
        return None

    async def update_cashe(self):
        while(True):
            del_list = []
            for resource_record in self.cashe:
                self.cashe[resource_record][1] -= self.upd_freq
                if(self.cashe[resource_record][1] <= 0):
                    del_list.append(resource_record)
            for rrtd in del_list:
                del self.cashe[rrtd]

            await asyncio.sleep(self.upd_freq)

    async def save_cashe(self,name):
        while(True):
            with open(name,'wb') as file:
                pickle.dump(self.cashe,file)
            await asyncio.sleep(10)

    def set_cashe(self,name):
        with open(name,'rb') as file:
            self.cashe=pickle.load(file)






class RecordInfo():
    def __init__(self,type,len,data):
        self.type = type
        self.length = len
        self.raw_data = data


