import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import validates

import components.validator as validator

RelationsBase = declarative_base()


# BaseModel class that provides common utility to all models
class BaseModel(object):
    # All tables should use the same storage engine
    __table_args__ = {'mysql_engine': 'InnoDB'}
    _remove_columns = []

    # All tables should contain these columns
    created_at = Column(DateTime, default=datetime.now)  # When it was created
    updated_at = Column(DateTime, onupdate=datetime.now)  # When it was created
    deleted_at = Column(DateTime)  # When it was deleted
    id = Column(Integer, primary_key=True)  # ID used for database relationships
    uuid = Column(String(length=50), unique=True, default=uuid.uuid4)  # UUID used as ID in applications

    def __init__(self, init=None):
        if init:
            self.load(init)

    def load(self, init=None):
        if init:
            for a in inspect(self).attrs.keys():
                if init.get(a):
                    setattr(self, a, init[a])

    def serialize(self, additional=[]):
        columns = {}
        for c in self.__table__.columns:
            if c.name in self._remove_columns:
                continue
            else:
                columns[c.name] = getattr(self, c.name)
        for c in additional:
            if hasattr(self, c):
                rel = getattr(self, c)
                if isinstance(rel, list):
                    relations = []
                    for r in rel:
                        relation = {}
                        for o in r.__table__.columns:
                            if o.name in r._remove_columns:
                                continue
                            else:
                                relation[o.name] = getattr(r, o.name)
                        relations.append(relation)
                    columns[c] = relations
                else:
                    relation = {}
                    for o in rel.__table__.columns:
                        if o.name in rel._remove_columns:
                            continue
                        else:
                            relation[o.name] = getattr(rel, o.name)
                    columns[c] = relation
        return columns

    @validates('created_at')
    def validate_int(self, key, value):
        validator.has_value(self, key, value)
        return validator.is_datetime(self, key, value)

    @validates('updated_at')
    def validate_int(self, key, value):
        validator.has_value(self, key, value)
        return validator.is_datetime(self, key, value)

    @validates('deleted_at')
    def validate_int(self, key, value):
        return validator.is_datetime(self, key, value)

    @validates('id')
    def validate_int(self, key, value):
        validator.has_value(self, key, value)
        return validator.is_int(self, key, value)

    @validates('uuid')
    def validate_string(self, key, value):
        validator.has_value(self, key, value)
        return validator.is_string(self, key, value)
