from singletone import singleton

@singleton
class DNSTransactionManager():
    def __init__(self):
        self.transaction_mem = dict()

    def check_transaction(self,transaction_id,addres):
        if(transaction_id in self.transaction_mem.keys()):
            ret_v = self.transaction_mem[transaction_id]
            del self.transaction_mem[transaction_id]
            return ret_v
        else:
            self.transaction_mem[transaction_id] = addres
            return None