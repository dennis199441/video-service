from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity
from app.decorators.role_required import role_required
from app.services.process_service import get_all_process_types, create_process_type, delete_process_type

ptype = Blueprint("ptype", __name__)


@ptype.route('/', methods=['GET'])
@jwt_required
def get():
    result, status = {}, 200
    try:
        result = get_all_process_types()
    except:
        result["message"] = "Get all roles error"
        status = 500
    return jsonify(result), status


@ptype.route('/', methods=['POST'])
@jwt_required
@role_required(["Admin"])
def create():
    name = request.form.get('name')
    result, status = {}, 201
    try:
        result = create_process_type(name)
    except:
        result["message"] = "Create process type error"
        status = 500
    return jsonify(result), status


@ptype.route('/<id>', methods=['DELETE'])
@jwt_required
@role_required(["Admin"])
def delete_by_id(id):
    result, status = {}, 204
    try:
        delete_process_type(id)
    except:
        result["message"] = "Delete process type error"
        status = 500
    return jsonify(result), status
