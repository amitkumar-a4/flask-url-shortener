from .. import db
from sqlalchemy.sql import func


class Url(db.Model):
    """ This class represents the urls table."""
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    rand_id = db.Column(db.String(7), index=True, unique=True)
    long_url = db.Column(db.Text, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
