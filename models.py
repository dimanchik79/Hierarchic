from peewee import *

"""В модуле реализованы модели базы банных
   с помощью библиотеки PEEWEE"""

DB = SqliteDatabase('DB/base.db')


class BaseModel(Model):
    class Meta:
        database = DB


class Bibliophile(BaseModel):
    bibl_name = CharField(max_length=1024, null=True)


class Hierarchic(BaseModel):
    bibl_id = IntegerField()
    items = CharField(max_length=1024, null=True)


class Data(BaseModel):
    unique = CharField(max_length=1024, null=True)
    field_name = CharField(max_length=1024, null=True)
    field_data = CharField(max_length=1024, null=True)
