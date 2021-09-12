from sqlalchemy import Column, String, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields


class Process(Entity, Base):
    __tablename__ = 'process'

    user_id = Column(Integer)
    type_id = Column(Integer, ForeignKey('process_types.id', ondelete='CASCADE'))
    filename = Column(String)
    hashed_name = Column(String)
    status = Column(String)

    def __init__(self, user_id, type_id, filename, hashed_name, status):
        Entity.__init__(self)
        self.user_id = user_id
        self.type_id = type_id
        self.filename = filename
        self.hashed_name = hashed_name
        self.status = status


class ProcessLogSchema(Schema):
    id = fields.Number()
    user_id = fields.Number()
    type_id = fields.Number()
    filename = fields.String()
    hashed_name = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
