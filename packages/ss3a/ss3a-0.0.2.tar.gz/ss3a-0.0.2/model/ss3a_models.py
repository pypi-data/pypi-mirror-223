from sqlalchemy import Column, String, Boolean, DateTime

from model import Base


class Ss3aMember(Base):
    __tablename__ = 'ss3a_member'
    id_ = Column('member_id', String(50), primary_key=True)
    password = Column('member_password', String(100))
    mobile = Column('mobile', String(10))
    email = Column('email', String(50))
    facebook_id = Column('facebook_id', String(50))
    line_id = Column('line_id', String(50))
    line_name = Column('line_name', String(50))
    name = Column('name', String(50))
    default_lang_code = Column('default_lang_code', String(10))
    enabled = Column('enabled', Boolean)
    last_login_date_time = Column('last_login_date_time', DateTime)
    enable_date = Column('enable_date', DateTime)
    disable_date = Column('disable_date', DateTime)
    create_time = Column('create_time', DateTime)
    update_time = Column('update_time', DateTime)
    creator = Column('creator', String(50))
    updater = Column('updater', String(50))

    def __init__(self, id_: str, password: str, mobile: str, email: str, facebook_id: str, line_name: str, name: str, default_lang_code: str, enabled: bool, last_login_date_time: str, enable_date: str, disable_date: str, create_time: str, update_time: str, creator: str, updater: str):
        self.id_ = id_
        self.password = password
        self.mobile = mobile
        self.email = email
        self.facebook_id = facebook_id
        self.line_name = line_name
        self.name = name
        self.default_lang_code = default_lang_code
        self.enabled = enabled
        self.last_login_date_time = last_login_date_time
        self.enable_date = enable_date
        self.disable_date = disable_date
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
