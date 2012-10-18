# encoding:utf-8 #
""" This module test all methods on ModelOne class """

from model_one import ModelOne
from nose.tools import assert_equals

OBJ1_ID, OBJ2_ID = None, None


class TestModelOne(object):
    """ Test all methods on ModelOne """

    @classmethod
    def setUpClass(cls):
        """SetupClass used to create two instances of ModelOne document """
        global OBJ1_ID, OBJ2_ID

        # Create two objects for test
        obj1 = ModelOne()
        obj1.int_value1 = 500
        obj1.int_value2 = 123
        obj1.boolean_value = True
        obj1.save()

        obj2 = ModelOne()
        obj2.int_value1 = 500
        obj2.int_value2 = 900
        obj2.boolean_value = False
        obj2.save()

        # Save the id of objects to match in the test
        OBJ1_ID = obj1.id
        OBJ2_ID = obj2.id

    def setUp(self):
        """ This method run on every test """

        self.obj1_id = OBJ1_ID
        self.obj2_id = OBJ2_ID

    def test_match_with_value1(self):
        "Should be match value 1 with ModelOne value """

        find = ModelOne.get_model_one_by_value1(500)
        assert_equals(len(find), 2)
        assert_equals(find[0].id, self.obj1_id)
        assert_equals(find[1].id, self.obj2_id)

    def test_match_with_boolean_value(self):
        "Should be match boolean with ModelOne value """

        find = ModelOne.get_model_one_by_boolean_value(True)
        assert_equals(len(find), 1)
        assert_equals(find[0].id, self.obj1_id)


class TestModelOneStep2(object):
    """ Test if database is clear.
        The option mongoengine-clear-after-class is active. """

    def test_match_with_value1(self):
        """Expected no results. """

        find = ModelOne.get_model_one_by_value1(500)
        assert_equals(len(find), 0)

    def test_match_with_boolean_value(self):
        """Expected no results. """

        find = ModelOne.get_model_one_by_boolean_value(True)
        assert_equals(len(find), 0)
