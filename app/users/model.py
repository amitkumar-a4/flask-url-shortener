from .. import db
from sqlalchemy.sql import func


class User(db.Model):
    """ This class represents the urls table."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_plaintext = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    urls = db.relationship('Url', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
