import sys
from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from app.decorators.role_required import role_required
from app.services.process_service import get_all_processes, get_process_by_id, create_process, cancel_process, upload_file, download_file

process = Blueprint("process", __name__)


@process.route('/', methods=['POST'])
@jwt_required
def create():
    user_id = request.form.get('user_id')
    type_id = request.form.get('type_id')
    file = request.files['file']
    result, status = {}, 201
    try:
        uploaded = upload_file(user_id, file)
        result = create_process(user_id, type_id, uploaded["filename"], uploaded["hash"])
    except:
        result["message"] = "Create process error"
        status = 500
    return jsonify(result), status


@process.route('/<id>', methods=['PUT'])
@jwt_required
def cancel(id):
    result, status = {}, 204
    try:
        cancel_process(id)
    except:
        result["message"] = "Cancel process error"
        status = 500
    return jsonify(result), status


@process.route('/<id>', methods=['GET'])
@jwt_required
def get_by_id(id):
    result, status = {}, 200
    try:
        result = get_process_by_id(id)
    except:
        result["message"] = "Get process by id error"
        status = 500
    return jsonify(result), status


@process.route('/', methods=['GET'])
@jwt_required
@role_required(["Admin"])
def get():
    result, status = {}, 200
    try:
        result = get_all_processes()
    except:
        result["message"] = "Get all processes error"
        status = 500
    return jsonify(result), status


@process.route('/download/<id>', methods=['GET'])
@jwt_required
def download(id):
    result, status = {}, 200
    try:
        return download_file(id)
    except:
        result["message"] = "Download file error"
        status = 500
    return jsonify(result), status