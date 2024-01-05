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
    path = TextField(null=True)                             # полный путь
    bibl_name = CharField(max_length=1024, null=True)       # название библитотеки
    parent = CharField(max_length=1024, null=True)          # родитель
    level = IntegerField(null=True)                         # уровень вложенности
    mark = IntegerField(null=True)                          # признак документ или каталог
    name_docum = CharField(max_length=1024, null=True)      # название название документа


class Data(BaseModel):
    bibl_name = CharField(max_length=1024, null=True)
    item_name = CharField(max_length=1024, null=True)
    field_name = CharField(max_length=1024, null=True)
    field_data = CharField(max_length=1024, null=True)


class Current(BaseModel):
    bibl_name = CharField(max_length=1024, null=True)   # название библитотеки
    level = IntegerField(null=True)                     # уровень
    parent = CharField(max_length=1024, null=True)      # родитель
    path = TextField(null=True)                         # полный путь
