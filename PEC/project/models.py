from PEC.database import db
from .status import Status
from sqlalchemy_utils import UUIDType
import uuid


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(UUIDType(), nullable=False, unique=True, index=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)