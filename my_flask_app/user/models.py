# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from my_flask_app.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from my_flask_app.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Role({name})>".format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)


class Domain(SurrogatePK, Model):
    """one domain(actually is an url.)"""
    __tablename__ = "domains"
    domain = Column(db.String(255), nullable=False)
    description = Column(db.Text, nullable=True)
    user_id = reference_col('users', nullable=False)

    user = relationship("User", backref="domains")

    @property
    def title(self):
        if self.history:
            return self.history[0].title if self.history[0].title else "空标题"
        else:
            return "没有抓取记录"

    @property
    def fetch_time(self):
        if self.history:
            return self.history[0].add_time
        else:
            return "没有抓取记录"


class FetchRecord(SurrogatePK, Model):
    """fetch record of domain"""
    __tablename__ = 'fetch_records'
    domain_id = reference_col("domains", nullable=False)
    title = Column(db.Text, nullable=True)
    headers = Column(db.Text, nullable=True)
    body = Column(db.Text, nullable=True)
    domain = relationship("Domain", backref="history", order_by='FetchRecord.add_time')
