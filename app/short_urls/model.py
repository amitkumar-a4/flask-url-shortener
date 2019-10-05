import secrets
from .. import db
from sqlalchemy.sql import func

MAX_LIMIT = 56000000000


class Url(db.Model):
    """ This class represents the urls table."""
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    # short_url = db.Column(db.String(7), index=True, unique=True)
    short_url = db.Column(db.String(80), unique=True)
    long_url = db.Column(db.Text, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Url {self.short_url}>'

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    @classmethod
    def get_by_short_url(cls, short_url):
        return cls.query.filter_by(short_url=short_url).first()

    @staticmethod
    def _rand_id():
        # Generate random int
        # 10000 to ensure at leas 3 char url after base62 conversion
        return str(secrets.randbelow(56000000000) + 10000)

    def to_dict(self):
        data = {
            'short_url': self.short_url
        }
        return data
