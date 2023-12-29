from bson import ObjectId
from django.urls import converters

class ObjectIDConverter(converters.StringConverter):
    regex = r'[0-9a-fA-F]{24}'

    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)