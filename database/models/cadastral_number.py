from dataclasses import dataclass
from playhouse.sqlite_ext import CharField
from .base import BaseModel


@dataclass
class Status:
    new: int
    sent: int
    error: int
    downloaded: int


class CadastralNumber(BaseModel):
    cadastral_number = CharField(max_length=32, primary_key=True)
    status = CharField(max_length=16, default='new')

    @classmethod
    def get_status(cls):
        status = Status(
            cls.select().where(CadastralNumber.status == 'new').count(),
            cls.select().where(CadastralNumber.status == 'sent').count(),
            cls.select().where(CadastralNumber.status == 'error').count(),
            cls.select().where(CadastralNumber.status == 'downloaded').count()
        )
        return status


CadastralNumber.create_table()
