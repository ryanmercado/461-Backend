from flask import Flask, request, jsonify
from flask import render_template
from pymongo import MongoClient
import json
import resourceDatabase


def get_project_name(project_id):
    name = ''
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    exists, proj_number = check_proj_exists(project_id)
    if not exists:
        return jsonify({'name': 'does not exist'})
    for collection in db.list_collection_names():
        col = db[collection].find_one({'proj_id': project_id})
        if col is not None:
            name = col['project_name']
    client.close()
    return jsonify({'name': name})


def create_project(name, proj_id, description):
    print('here')
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    print('here2')
    exists, proj_number = check_proj_exists(proj_id)
    print('got proj_numer and exists')
    if exists:
        return jsonify({'result': 'Project ID exists'})
    print('passed the if')
    collection = db['Project' + str(proj_number+1)]
    print('got past exist statement')
    new_document = {
        "project_name": name,
        "proj_id": proj_id,
        "description": description
    }
    print('Project' + str(proj_number+1))
    collection.insert_one(new_document)
    print('inserted')
    client.close()
    return jsonify({'result': 'Project Created'})


def check_proj_exists(proj_id):
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    count = 0
    for collection_name in db.list_collection_names():
        count += 1
        collection = db[collection_name]
        project = collection.find_one({'proj_id': proj_id})
        if project is not None:
            return True, count
    client.close()
    return False, count


def add_resource(proj_id, resource_name, qty):
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    exists, proj_number = check_proj_exists(proj_id)
    if not exists:
        return jsonify({'result': 'Project does not exist'})
    project = db['Project' + str(proj_number)]
    document = project.find_one({resource_name: {"$exists": True}})
    if document is None:
        project.insert_one({resource_name: qty})
    else:
        project.update_one(
            {"_id": document["_id"]},
            {"$inc": {resource_name: qty}}
        )
    client.close()
    return jsonify({'result': 'Resource added'})


def check_out_resources(resource_name, quantity, project_id):
    print("name: " + resource_name + ". quantity: " + quantity + ". projectId: " + project_id)
    allowed = resourceDatabase.checkOut(resource_name, quantity)
    if allowed != 'allowed':
        return jsonify({'result': allowed})
    right_collection = None
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    count = 0
    for collection in db.list_collection_names():
        count += 1
        col = db[collection].find_one({'proj_id': project_id})
        if col is not None:
            right_collection = db[collection]
            break
    res = right_collection.find_one({'res_name': resource_name})
    if res is None:
        print('right spot')
        new_document = {
            'res_name': resource_name,
            'checkedOut': int(quantity)
        }
        right_collection.insert_one(new_document)
    else:
        right_collection.update_one(
            {'res_name': resource_name},
            {'$inc': {'checkedOut': int(quantity)}}
        )
    client.close()
    return jsonify({'result': 'Resources checked out!'})


def check_in_resources(resource_name, quantity, projectId):
    right_collection = None
    print(resource_name)
    client = MongoClient("mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites"
                         "=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    for collection in db.list_collection_names():
        col = db[collection].find_one({'proj_id': projectId})
        if col is not None:
            right_collection = db[collection]
            break
    res = right_collection.find_one({'res_name': resource_name})
    if res is None:
        client.close()
        print('first you dont have that many')
        return jsonify({'result': 'You do not have that many!'})
    elif res is not None:
        inv = res['checkedOut']
        print(inv)
        if int(quantity) > inv:
            client.close()
            print('second you dont have that many')
            return jsonify({'result': 'You do not have that many!'})
        else:
            new_inv = inv - int(quantity)
            print('updating projectDatabse. New inv: ' + str(new_inv))
            right_collection.update_one(
                {'res_name': resource_name},
                {'$inc': {'checkedOut': -(int(quantity))}}
            )
            resourceDatabase.checkIn(resource_name, int(quantity))
            client.close()
            return jsonify({'result': 'Resources checked in!'})
    client.close()
    return jsonify({'result': 'ProjID not Found'})


def log_into_project(project_id):
    client = MongoClient(
        "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
    db = client.Projects
    exists, proj_number = check_proj_exists(project_id)
    if not exists:
        return jsonify({'result': 'Project ID does not exist', 'id': '000'})
    client.close()
    return jsonify({'result': 'Signed into project', 'id': project_id})


def get_project_resources(project_id):
    print("im in get_project_resources" + project_id)
    resourceDatabase.get_resource_availability()
    arr = resourceDatabase.get_resources_list()
    new_arr = []
    right_collection = None
    try:
        client = MongoClient(
            "mongodb+srv://graysondrinkard:grayson_drinkard34@cluster0.lx1r67n.mongodb.net/?retryWrites=true&w=majority",
            tls=True, tlsAllowInvalidCertificates=True)
        db = client.Projects
        count = 0
        for collection in db.list_collection_names():
            count += 1
            col = db[collection].find_one({'proj_id': project_id})
            if col is not None:
                right_collection = db[collection]
                break

        for name in arr:
            name = name[0].upper() + name[1:]
            doc = right_collection.find_one({'res_name': name})
            if doc is None:
                new_arr.append(0)
            else:
                new_arr.append(doc['checkedOut'])
    except Exception as e:
        print(f"Error while querying collection '{project_id}': {str(e)}")
    print(new_arr)
    client.close()
    return json.dumps(new_arr)

