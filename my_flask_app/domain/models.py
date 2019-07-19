from my_flask_app.database import Model, SurrogatePK, Column
from my_flask_app.extensions import db


class Domain(SurrogatePK, Model):
    __tablename__ = "users"
    domain = Column(db.String(255), nullable=False)
    description = Column(db.Text, nullable=True)
    user_id = Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", backref="domains")
