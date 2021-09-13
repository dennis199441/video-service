from datetime import datetime
from flask import send_from_directory
from app.entities.entity import Session
from app.entities.process import Process, ProcessLogSchema
from app.entities.process_types import ProcessType, ProcessTypeSchema
from app.utils.process_status import ProcessStatus
import hashlib
import time
import os

ALLOWED_EXTENSIONS = {'mov', 'mp4'}
UPLOAD_FOLDER = "/usr/src/app/input"
OUTPUT_FOLDER = "/usr/src/app/output"


def get_all_process_types():
    session = Session()
    ptype_obj = session.query(ProcessType)
    schema = ProcessTypeSchema(many=True)
    ptype = schema.dump(ptype_obj)
    session.close()
    return ptype.data


def create_process_type(name):
    session = Session()
    ptype_obj = ProcessType(name)
    session.add(ptype_obj)
    session.commit()
    schema = ProcessTypeSchema(many=False)
    ptype = schema.dump(ptype_obj)
    session.close()
    return ptype.data


def delete_process_type(id):
    session = Session()
    ptype = session.query(ProcessType).filter_by(id=id).first()
    session.delete(ptype)
    session.commit()
    session.close()


def get_all_processes():
    session = Session()
    process_obj = session.query(Process)
    schema = ProcessLogSchema(many=True)
    process = schema.dump(process_obj)
    session.close()
    return process.data


def get_processes_by_type(type_id):
    session = Session()
    process_obj = session.query(Process)\
    .filter_by(type_id=type_id)\
    .filter_by(status=ProcessStatus.QUEUED.name)\
    .order_by(Process.updated_at)
    schema = ProcessLogSchema(many=True)
    process = schema.dump(process_obj)
    session.close()
    return process.data


def get_process_by_id(id):
    session = Session()
    process_obj = session.query(Process).filter_by(id=id).first()
    schema = ProcessLogSchema(many=False)
    process = schema.dump(process_obj)
    session.close()
    return process.data


def create_process(user_id, type_id, filename, hash):
    session = Session()
    process_obj = Process(user_id, type_id, filename,
                          hash, ProcessStatus.QUEUED.name)
    session.add(process_obj)
    session.commit()
    schema = ProcessLogSchema(many=False)
    process = schema.dump(process_obj)
    session.close()
    return process.data


def cancel_process(id):
    now = datetime.now()
    session = Session()
    process_obj = session.query(Process).filter_by(id=id)
    if process_obj.count() == 1:
        process_obj.update(
            {Process.status: ProcessStatus.CANCELLED.name, Process.updated_at: now}, synchronize_session='fetch')
        session.commit()
    session.close()


def run_process(id):
    now = datetime.now()
    session = Session()
    process_obj = session.query(Process).filter_by(id=id)
    if process_obj.count() == 1:
        process_obj.update(
            {Process.status: ProcessStatus.RUNNING.name, Process.updated_at: now}, synchronize_session='fetch')
        session.commit()
    session.close()
   
   
def complete_process(id):
    now = datetime.now()
    session = Session()
    process_obj = session.query(Process).filter_by(id=id)
    if process_obj.count() == 1:
        process_obj.update(
            {Process.status: ProcessStatus.COMPLETED.name, Process.updated_at: now}, synchronize_session='fetch')
        session.commit()
    session.close()
     
    
def upload_file(user_id, file):
    if not validate_file(file.filename):
        raise Exception('unsupported type')
    now = str(time.time())
    user_id_str = str(user_id)
    raw = bytes(user_id_str + "_" + file.filename +
                "_" + now, encoding='utf-8')
    hash = hashlib.sha224(raw).hexdigest()
    filename = hash + "-" + file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return {"hash": hash, "filename": file.filename}


def validate_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def download_file(id):
    process = get_process_by_id(id)
    filename = process["hashed_name"] + "-" + process["filename"]
    return send_from_directory(directory=OUTPUT_FOLDER, filename=filename)