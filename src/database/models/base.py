from datetime import datetime
from playhouse.sqlite_ext import DateTimeField, Model
from ..database import database

class BaseModel(Model):
    class Meta:
        database = database
    created_at = DateTimeField(
        formats=['%Y-%m-%d %H:%M:%S'],
        default=datetime.now
    )
