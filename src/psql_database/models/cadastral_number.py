from playhouse.sqlite_ext import CharField
from .base import BaseModel
from ..database import database

class Status:
    def __init__(self, total, loaded, sent, received, error) -> None:
        self.total = total
        self.loaded = loaded
        self.sent = sent
        self.received = received
        self.error = error

class CadastralNumber(BaseModel):
    cadastral_number = CharField(max_length=32, primary_key=True)
    status = CharField(max_length=16, default='loaded')

    @classmethod
    def get_statuses(cls):
        # database.connect()
        status = Status(
            cls.select().count(),
            cls.select().where(CadastralNumber.status == 'loaded').count(),
            cls.select().where(CadastralNumber.status == 'sent').count(),
            cls.select().where(CadastralNumber.status == 'received').count(),
            cls.select().where(CadastralNumber.status == 'error').count()
        )
        # database.close()
        return status
    
    @classmethod
    def reset_all(cls):
        # database.connect()
        for num in cls.select():
            num.status = 'loaded'
            num.save()
        # database.close()

CadastralNumber.create_table()