from flask import Flask, request, jsonify
from flask_cors import CORS
import userDatabase
import projectDatabase
import resourceDatabase

app = Flask(__name__)
CORS(app)


@app.route('/api/user-create-account', methods=['POST'])
def create_account():
    return userDatabase.create_account(request.json['username'], request.json['password'],
                                       request.json['confirmPassword'])


@app.route('/api/get-name', methods=['POST'])
def get_project_name():
    return projectDatabase.get_project_name(request.json['projectId'])


@app.route('/api/create-project', methods=['POST'])
def create_project():
    return projectDatabase.create_project(request.json['name'], request.json['project_id'], request.json['description'])


@app.route('/api/get_project_resources', methods=['POST'])
def get_project_resources():
    return jsonify(projectDatabase.get_project_resources(request.json['projectId']))  # need to return an array of ints


@app.route('/api/get_resource_availability', methods=['POST'])
def get_resource_availability():
    return jsonify(resourceDatabase.get_resource_availability())  # need to return an array of ints


@app.route('/api/getResources', methods=['POST'])
def get_resources():
    return jsonify(resourceDatabase.get_resources())  # need to return an array of strings


@app.route('/api/handleCheckIn', methods=['POST'])
def check_in_resources():
    return projectDatabase.check_in_resources(request.json['name'], request.json['quantity'], request.json['projectId'])


@app.route('/api/project-login-attempt', methods=['POST'])
def log_into_project():
    return projectDatabase.log_into_project(request.json['projId'])


@app.route('/api/handleCheckout', methods=['POST'])
def check_out_resources():
    print('about to checkout')
    quan = request.json['quantity']
    print('got quan: ' + quan)
    name = request.json['name']
    print('got name: ' + name)
    return projectDatabase.check_out_resources(name, quan, request.json['projectId'])


@app.route('/api/user-login-attempt', methods=['POST'])
def login():
    print('login attempt')
    return userDatabase.login(request.json['username'], request.json['password'])


if __name__ == '__main__':
    app.run()
