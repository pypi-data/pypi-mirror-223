# -*- coding: utf-8 -*-
"""


Author: ken
Date: 2023/7/18
"""

from sqlalchemy import Connection, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapper
from ss3a_model import model_utilty


Base = declarative_base()


class GenericEntity(Base):
    __abstract__ = True
    prefix = None
    number_length = 0
    sequence_name = None

    def __init__(self):
        pass

    @classmethod
    def generate_id(cls, conn: Connection):
        available: bool = False
        new_id: str = None
        while not available:
            new_id = cls.generate_id_internal(conn)
            if not cls.check_if_id_exist(conn, new_id):
                available = True

        return new_id

    @classmethod
    def generate_id_internal(cls, conn: Connection):
        stmt = text('select next_val from hibernate_sequence where sequence_name = :sequence_name')
        result = conn.execute(stmt, {'sequence_name': cls.sequence_name}).scalar_one()
        generated_id = cls.prefix + str(result).zfill(cls.number_length)
        stmt = text('update hibernate_sequence set next_val = :new_num where sequence_name = :sequence_name')
        conn.execute(stmt, {'new_num': result+1, 'sequence_name': cls.sequence_name})
        return generated_id

    @classmethod
    def check_if_id_exist(cls, conn: Connection, generated_id: str) -> bool:
        entity = cls.query.filter(cls.id_ == generated_id).first()
        if entity:
            return True
        else:
            return False


@event.listens_for(Mapper, 'before_insert')
def generate_user_id(mapper, conn, target):
    target.id_ = target.generate_id(conn)
