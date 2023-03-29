from flask import Flask, request, jsonify
from flask import render_template
from pymongo import MongoClient
from cipher import encrypt


def create_account(username, password, password2):
    print('creating the account')
    client = MongoClient("mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
                         tls=True, tlsAllowInvalidCertificates=True)
    db = client.Users
    if password2 != password:
        return jsonify({'result': 'Passwords do not match'})
    password = encrypt(password, 3, 1)
    count = 0
    for collection_name in db.list_collection_names():
        count += 1
        collection = db[collection_name]
        user = collection.find_one({'userid': username})
        if user is not None:
            return jsonify({'result': 'Username Exists'})
    collection = db['User'+str(count+1)]
    new_document = {
        "userid": username,
        "password": password
    }
    collection.insert_one(new_document)
    client.close()
    return jsonify({'result': 'Account Created'})


def login(username, password):
    print("login")
    client = MongoClient("mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
                         tls=True, tlsAllowInvalidCertificates=True)
    db = client.Users
    encrypted_password = encrypt(password, 3, 1)
    authorized = False
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        user = collection.find_one({'userid': username, 'password': encrypted_password})
        if user is not None:
            authorized = True
            break
    client.close()
    if authorized:
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})

