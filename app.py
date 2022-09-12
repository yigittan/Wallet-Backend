from flask import Flask , request , jsonify
from flask_pymongo import PyMongo
from store import WalletMongoStorage
from wallet import WalletService
from bson.objectid import ObjectId

app = Flask(__name__)

mongodb_client = PyMongo(app,uri="mongodb://localhost:27017/wallets")

storage = WalletMongoStorage(mongodb_client)
service = WalletService(storage)

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NO_CONTENT = 204
STATUS_BAD_REQUEST = 400
STATUS_INTERNAL_SERVER_ERROR = 500
STATUS_NOT_FOUND = 404

def http_error_handler(func):

    def create_err_msg(err):
        return {'message':str(err)}

    def handler(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except ValueError as e:
            return create_err_msg(e) , STATUS_BAD_REQUEST
        except Exception as e:
            return create_err_msg(e) , STATUS_INTERNAL_SERVER_ERROR
    return handler

@app.route('/') # İT İS WORKİNG 
def index():
    return {'message':"Welcome to the index page"}

@app.route('/v1/wallets', methods=['POST'], endpoint='create') # İT İS WORKİNG 
@http_error_handler
def create():
    body = request.get_json()
    name = body['name']
    email = body['email']
    password = body['password']

    id = service.create(name,email,password)
    print(id)


    return {'id':str(ObjectId(id))}, STATUS_CREATED

@app.route('/v1/wallets',methods=['GET'],endpoint='get_all_wallet') # İT İS WORKİNG
@http_error_handler
def get_all_wallet():
    wallets = service.get_all()
    return jsonify(wallets), STATUS_OK

@app.route('/v1/wallets/<string:id>', methods=['GET'],endpoint='get_wallet') # İT İS WORKİNG 
@http_error_handler
def get_wallet(id):
    id = ObjectId(id)
    wallet = service.get_by_id(id)
    return jsonify(wallet),STATUS_OK

@app.route('/v1/wallets/by/<string:email>',methods=['GET'] , endpoint='get_by_email') # İT İS WORKİNG
@http_error_handler
def get_by_email(email):
    wallet = service.get_by_email(email)
    return jsonify(wallet),STATUS_OK

@app.route('/v1/wallets/<string:id>/transfer',methods=['PUT'], endpoint ='transfer')
@http_error_handler
def transfer(id):
    body = request.get_json()
    amount = body['amount']
    to = body['to']
    service.transfer(id,amount,to)
    wallet = service.get_by_id(id)
    return jsonify(wallet),STATUS_OK

@app.route('/v1/wallets/<string:id>/withdraw' , methods= ['PUT'], endpoint = 'withdraw')
@http_error_handler
def withdraw(id):
    body = request.get_json()
    amount = body['amount']
    transaction = service.withdraw(id,amount)
    return jsonify(transaction), STATUS_OK

@app.route('/v1/wallets/<string:id>/deposit' , methods=['PUT'],endpoint='deposit')
@http_error_handler
def deposit(id):
    body = request.get_json()
    amount = body['amount']
    service.deposit(id,amount)

@app.route('/v1/wallets/<string:id>/delete' , methods=['DELETE'])
@http_error_handler
def delete(id):
    service.delete(id)
    return {'message':f'{id} id sine sahip wallet silindi'}

if __name__ == "__main__":
    app.secret_key ="01234"
    app.run(debug=True,host="127.0.0.1",port=3000)