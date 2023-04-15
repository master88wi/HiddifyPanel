import datetime
import uuid as uuid_mod

from sqlalchemy_serializer import SerializerMixin
from dateutil import relativedelta
from hiddifypanel.panel.database import db
from enum import auto
from strenum import StrEnum


class AdminMode(StrEnum):
    """
    The "UserMode" class is an enumeration that defines five possible modes: "no_reset", "monthly", "weekly",
    "daily", and "disable". These modes represent different settings that can be applied to a user account,
    such as the frequency at which data is reset or whether the account is currently disabled. The class is
    implemented using the "StrEnum" base class and the "auto()" function to generate unique values for each mode.
    """
    super_admin = auto()
    admin = auto()
    slave = auto()
    


class AdminUser(db.Model, SerializerMixin):
    """
    This is a model class for a user in a database that includes columns for their ID, UUID, name, online status,
    account expiration date, usage limit, package days, mode, start date, current usage, last reset time, and comment.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid_mod.uuid4()), nullable=False, unique=True)
    name = db.Column(db.String(512), nullable=False)
    mode = db.Column(db.Enum(AdminMode), default=AdminMode.slave,nullable=False)
    comment = db.Column(db.String(512))
    telegram_id=db.Column(db.String(512))
    users = db.relationship('User',backref='admin')
    usages = db.relationship('DailyUsage',backref='admin')
    def __str__(self):
        return str(self.name)

def get_super_admin_secret():
    admin=AdminUser.query.filter(AdminUser.mode==AdminMode.super_admin).first()
    if not admin:
        db.session.add(AdminUser(mode=AdminMode.super_admin))
        db.session.commit()
        admin=AdminUser.query.filter(AdminUser.mode==AdminMode.super_admin).first()
        
    admin_secret=admin.uuid
    return admin_secret


def get_admin_user_db(uuid):
    return AdminUser.query.filter(AdminUser.uuid==uuid).first()