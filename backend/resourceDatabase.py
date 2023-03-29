from flask import Flask, request, jsonify
from flask import render_template
from pymongo import MongoClient
import json


def get_resources_list():
    arr = []
    try:
        client = MongoClient(
            "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
            tls=True, tlsAllowInvalidCertificates=True)
        db = client.Resources
        for name in db.list_collection_names():
            collection = db[name]
            document = collection.find_one({})
            arr.append(document['name'])
    except Exception as e:
        client.close()
        print(f"Error connecting to database: {str(e)}")
    client.close()
    return arr


def get_resources():
    arr = []
    try:
        client = MongoClient(
            "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
            tls=True, tlsAllowInvalidCertificates=True)
        db = client.Resources
        for name in db.list_collection_names():
            collection = db[name]
            document = collection.find_one({})
            arr.append(document['name'])
    except Exception as e:
        client.close()
        print(f"Error connecting to database: {str(e)}")
    client.close()
    return json.dumps(arr)


def get_resource_availability():
    print('im in get-resource-availability')
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    arr = []
    db = client.Resources
    for name in db.list_collection_names():
        collection = db[name]
        document = collection.find_one({})
        arr.append(document['available'])
    print(arr)
    client.close()
    return json.dumps(arr)


def checkOut(resource, quantity):
    print('in the checkOut function in resourceDatabase')
    resource = resource[0].lower() + resource[1:]
    right_document = None
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Resources
    collection = None
    for name in db.list_collection_names():
        collection = db[name]
        document = collection.find_one({'name': resource})
        if document is not None:
            right_document = document
            break
    if right_document is None:
        client.close()
        return 'resource not found'

    print(right_document['available'])
    if 'available' in right_document and right_document['available'] >= int(quantity):
        collection.update_one({'_id': right_document['_id']}, {'$inc': {'available': -int(quantity)}})
        print('about to return true')
        client.close()
        return 'allowed'
    else:
        client.close()
        return 'Not enough of this resource available!'


def checkIn(resource, quantity):
    resource = resource[0].lower() + resource[1:]
    right_document = None
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Resources
    collection = None
    for name in db.list_collection_names():
        collection = db[name]
        document = collection.find_one({'name': resource})
        if document is not None:
            right_document = document
            break
    if right_document is None:
        client.close()
        return 'resource not found'
    print('updating')
    collection.update_one({'_id': right_document['_id']}, {'$inc': {'available': int(quantity)}})
    client.close()
    return 'allowed'


