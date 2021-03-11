import json
from pathlib import Path
from typing import List

from peewee import BooleanField, CharField, Model, ModelBase, SqliteDatabase

from certifications.config import DB_PATH, JSON_PATH


database = SqliteDatabase(str(DB_PATH))


def get():
    return database


class BaseModel(Model):
    class Meta:
        database = database

    def refresh(self) -> 'BaseModel':
        return type(self).get(self._pk_expr())


class User(BaseModel):
    username = CharField(unique=True)
    fullname = CharField()
    mail = CharField(unique=True)
    github = CharField(unique=True)
    honors = BooleanField(unique=True)

    @classmethod
    def load_from_json(cls, path: Path) -> None:
        if not path.is_file():
            raise ValueError("Can't find the student's JSON file.")
        users = json.loads(path.read_text())
        with database.atomic():
            for user in users:
                cls.insert(**user).on_conflict_ignore()


def bootstrap(models: List[ModelBase], students_json: Path) -> None:
    with database.connection_context():
        database.create_tables(models, safe=True)

    User.load_from_json(students_json)


ALL_MODELS = [User]
bootstrap(ALL_MODELS, JSON_PATH)
