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
    bibl_name = CharField(max_length=1024, null=True)
    items = TextField(null=True)


class Data(BaseModel):
    bibl_name = CharField(max_length=1024, null=True)
    item_name = CharField(max_length=1024, null=True)
    field_name = CharField(max_length=1024, null=True)
    field_data = CharField(max_length=1024, null=True)


class Current(BaseModel):
    bibl_name = CharField(max_length=1024, null=True)
