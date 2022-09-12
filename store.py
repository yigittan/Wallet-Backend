from bson.objectid import ObjectId

class WalletMongoStorage:
    def __init__(self,client):
        self.db = client.db.wallets

    def insert(self,name,email,password):
        res = self.db.insert_one({
            "name":name,
            "email":email,
            "password":password,
            "balance":0.00
        })
        return res.inserted_id

    def get_all(self):
        wallets = self.db.find()
        return [{
            "id":str(wallet['_id']),
            "email":wallet['email'],
            "balance":wallet['balance'],
        } for wallet in wallets]
    
    def get_by_id(self,id):
        wallet = self.db.find_one({'_id':ObjectId(id)})
        return {
            "id":str(ObjectId(wallet['_id'])),
            "name":wallet['name'],
            "balance":wallet['balance']
        }

    def get_by_email(self,email):
        wallet = self.db.find_one({'email':email})
        return {
            "id":str(ObjectId(wallet['_id'])),
            "name":wallet['name'],
            "balance":wallet['balance']
        }

    def transfer(self,id,amount,to):
        wallet = self.db.find_one({'_id':id})
        recipient_wallet = self.db.find_one({'_id':to})
        wallet['balance'] -= amount
        recipient_wallet['balance'] += amount
        self.db.update_one({'_id':id},{"$set":{"balance":wallet['balance']}})
        self.db.update_one({'_id':to}, {"$set": {"balance":recipient_wallet['balance']}})
        return {
            "id":str(ObjectId(wallet['_id'])),
            "name":wallet['name'],
            "balance":wallet['balance']
        }

    def withdraw(self,id,amount):
        id = ObjectId(id)
        wallet = self.db.find_one({'_id':id})
        wallet['balance'] -= amount
        self.db.update_one({'_id':id}, {"$set":{"balance":wallet['balance']}})

    def deposit(self,id,amount):
        wallet = self.db.find_one({'_id':id})
        wallet['balance'] += amount
        self.db.update_one({'_id':id}, {"$set":{"balance":wallet['balance']}})