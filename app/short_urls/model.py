import secrets
from app import db
from sqlalchemy.sql import func
from app.utils.short_url import ShortURL
MAX_LIMIT = 56000000000


class Url(db.Model):
    """ This class represents the urls table."""
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.BigInteger, unique=True)
    long_url = db.Column(db.Text, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Url {self.short_id}>'

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    @classmethod
    def get_by_short_url(cls, short_url):
        short_id = Url._decode(short_url)
        return cls.query.filter_by(short_id=short_id).first()

    @staticmethod
    def create_id():
        # Generate random int
        # 10000 to ensure at leas 3 char url after base62 conversion
        return secrets.randbelow(56000000000) + 10000

    @staticmethod
    def _encode_id(int):
        return ShortURL().encode(int)

    @staticmethod
    def _decode(str):
        return ShortURL().decode(str)

    def get_short_url(self):
        return Url._encode_id(self.short_id)
