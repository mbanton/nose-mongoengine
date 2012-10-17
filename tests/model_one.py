# encoding:utf-8 #
"""
Test model using model engine, this model has two int values and
a boolean value
"""

from mongoengine import Document, IntField, BooleanField


class ModelOne(Document):
    """ A sample model class """
    int_value1 = IntField()
    int_value2 = IntField()
    boolean_value = BooleanField(required=True, default=False)

    @classmethod
    def get_model_one_by_value1(cls, value):
        """Class method to get objects by value one """
        return cls.objects(int_value1=value)

    @classmethod
    def get_model_one_by_boolean_value(cls, value):
        """Class method to get objects by boolean value """
        return cls.objects(boolean_value=value)
