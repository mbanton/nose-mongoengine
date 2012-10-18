# encoding:utf-8 #
""" Test if database is clear. The option mongoengine-clear-after-module
is active. """

from model_one import ModelOne
from nose.tools import assert_equals

class TestModelOneEmpty(object):
    """ Test if database is clear. 
        The option mongoengine-clear-after-module is active. """

    def test_match_with_value1(self):
        """Expected no results. """

        find = ModelOne.get_model_one_by_value1(500)
        assert_equals(len(find), 0)

    def test_match_with_boolean_value(self):
        """Expected no results. """

        find = ModelOne.get_model_one_by_boolean_value(True)
        assert_equals(len(find), 0)
