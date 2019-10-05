from argon2 import PasswordHasher
from sqlalchemy.sql import func

from .. import db

ph = PasswordHasher()


class User(db.Model):
    """ This class represents the urls table."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    urls = db.relationship('Url', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def __init__(self, email, password):
        self.email = email
        self.password = ph.hash(password)

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def check_password(self, password):
        return ph.verify(self.password, password)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
