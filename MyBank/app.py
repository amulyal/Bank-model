from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from Models.Customer import Customer

app = Flask(__name__)
# connection string (host name, user id, password, database name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://amulya:Kimyeontan@localhost:5432/MyBank'

MyBankDb = SQLAlchemy(app)


@app.route("/customers", methods=['GET'])
def getCustomers():
    customers = MyBankDb.session.query(Customer).all()
    response = []
    for customer in customers:
        response.append({
            "id": customer.id,
            "firstName": customer.first_name,
            "lastName": customer.last_name,
            "dateOfBirth": customer.date_of_birth,
            "address": customer.address
        })
    return make_response(jsonify(response), 200)


@app.route("/customers/<int:id>", methods=['GET'])
def getCustomer(id):
    if MyBankDb.session.query(Customer.id).filter_by(id=id).scalar() is None:
        return make_response(jsonify({"message": "Customer Not Found"}), 404)

    customer = MyBankDb.session.query(Customer).filter(Customer.id == id).first()
    response = {
        "id": customer.id,
        "firstName": customer.first_name,
        "lastName": customer.last_name,
        "dateOfBirth": customer.date_of_birth,
        "address": customer.address
    }
    return make_response(jsonify(response), 200)


@app.route("/customers", methods=['POST'])
def addCustomer():
    data = request.get_json()
    customer = Customer(data['firstName'], data['lastName'], data['dateOfBirth'], data['address'])
    MyBankDb.session.add(customer)
    MyBankDb.session.commit()
    return make_response(jsonify({"message": "Customer Added"}), 201)


@app.route("/customers/<int:id>", methods=['PUT'])
def appendCustomer(id):
    if MyBankDb.session.query(Customer.id).filter_by(id=id).scalar() is None:
        return make_response(jsonify({"message": "Customer Not Found"}), 404)

    data = request.get_json()
    customer = MyBankDb.session.query(Customer).filter(Customer.id == id).first()
    customer.first_name = data['firstName']
    customer.last_name = data['lastName']
    customer.date_of_birth = data['dateOfBirth']
    customer.address = data['address']
    MyBankDb.session.commit()
    return make_response(jsonify({"message": "Customer Updated"}), 200)


@app.route("/customers/<int:id>", methods=['DELETE'])
def deleteCustomer(id):
    if MyBankDb.session.query(Customer.id).filter_by(id=id).scalar() is None:
        return make_response(jsonify({"message": "Customer Not Found"}), 404)

    MyBankDb.session.query(Customer).filter(Customer.id == id).delete()
    MyBankDb.session.commit()
    return make_response(jsonify({"message": "Customer Deleted"}), 200)


app.run(port=6000)
