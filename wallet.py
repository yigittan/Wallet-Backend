import bcrypt
from flask import jsonify

class WalletService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,name,email,password):
        byte_pass = password.encode('utf-8')
        hash = bcrypt.hashpw(byte_pass,bcrypt.gensalt())

        return self.storage.insert(name,email,hash)

    def get_all(self):
        return self.storage.get_all()

    def get(self,id):
        wallet = self.storage.get(id)
        if wallet is None:
            return {'message':'wallet not found'}
        return {'name':wallet['name']}

    def get_by_email(self,email):
        wallet = self.storage.get_by_email(email)
        return {'name':wallet['name']}

    def transfer(self,id,amount,to):
        wallet = self.storage.get(id)
        self.storage.transfer(id,amount,to)
        return {'name':wallet['name']}

    def withdraw(self,id,amount):
        wallet = self.storage.get(id)
        self.storage.withdraw(id,amount)
        return {'name':wallet['name']}

    def deposit(self,id,amount):
        wallet = self.storage.get(id)
        self.storage.deposit(id,amount)
        return {'name':wallet['name']}
        

    