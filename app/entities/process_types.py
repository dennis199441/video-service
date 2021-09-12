from sqlalchemy import Column, String, Integer
from .entity import Entity, Base, engine
from marshmallow import Schema, fields


class ProcessType(Entity, Base):
    __tablename__ = 'process_types'

    name = Column(String, unique=True)

    def __init__(self, name):
        Entity.__init__(self)
        self.name = name


class ProcessTypeSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
