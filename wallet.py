import bcrypt
from flask import jsonify
from bson.objectid import ObjectId

class WalletService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,name,email,password):
        byte_pass = password.encode('utf-8')
        hash = bcrypt.hashpw(byte_pass,bcrypt.gensalt())

        return self.storage.insert(name,email,hash)

    def get_all(self):
        return self.storage.get_all()

    def get_by_id(self,id):
        wallet = self.storage.get_by_id(id)
        if wallet is None:
            return {'message':'wallet not found'}
        return wallet

    def get_by_email(self,email):
        wallet = self.storage.get_by_email(email)
        return wallet

    def transfer(self,id,amount,to):
        id = ObjectId(id)
        to = ObjectId(to)
        wallet = self.storage.get_by_id(id)
        self.storage.transfer(id,amount,to)
        return wallet

    def withdraw(self,id,amount):
        id = ObjectId(id)
        self.storage.withdraw(id,amount)
        wallet = self.storage.get_by_id(id)
        return wallet

    def deposit(self,id,amount):
        self.storage.deposit(id,amount)
        wallet = self.storage.get_by_id(id)
        return wallet
        

    