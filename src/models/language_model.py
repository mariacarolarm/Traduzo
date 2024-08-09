from database.db import db
from models.abstract_model import AbstractModel


class LanguageModel(AbstractModel):
    _collection = db["languages"]

    def __init__(self, json_data):
        self.data = json_data

    def to_dict(self):
        return {
            'name': self.data['name'],
            'acronym': self.data['acronym'],
        }

    @classmethod
    def list_dicts(cls):
        data = cls._collection.find()
        return [
            {
                'name': language['name'],
                'acronym': language['acronym'],
                '_id': language['_id']
            }
            for language in data
        ]
