================
nose-mongoengine
================

A nose plugin to facilitate the creation of automated tests that access Mongo Engine structures.

Originally based on Mongo Nose ( http://pypi.python.org/pypi/mongonose/ ). Thanks to: Kapil Thangavelu


Source: https://github.com/mbanton/nose-mongoengine/
Pypi page: http://pypi.python.org/pypi/nose-mongoengine/


Installation
============

Using pip:

    pip install nose-mongoengine

Configuration
=====

The plugin extends the nose options with a few options. The only
required options are either `--mongoengine` or `--mongoengine-mongodb-bin` to enable
the plugin.

 - `--mongoengine` is required to enable the plugin.

 - `--mongoengine-mongodb-bin` Allows specifying the path to the `mongod` binary.
   If not specified the plugin will search the path for a mongodb
   binary. If one is not found, an error will be raised.

 - `--mongoengine-clear-after-module` Optionally clear data in db after every module of tests.

 - `--mongoengine-clear-after-class` Optionally clear data in db after every class of tests.

 - `--mongoengine-mongodb-port` can be optionally set, by default the plugin
   will utilize a a random open port on the machine.

 - `--mongoengine-mongodb-scripting` Enables the javascript scripting engine,
   off by default.

 - `--mongoengine-mongodb-logpath` Stores the server log at the given path, by
   default sent to /dev/null

 - `--mongoengine-mongodb-prealloc` Enables pre-allocation of databases, default
   is off. Modern filesystems will sparsely allocate, which can
   speed up test execution.


The plugin will up a instance of Mongo Db and create a empty database to use it.


Usage in your test cases
=====

Since this is your model using mongoengine ( model_one.py )

``` python
# encoding:utf-8 #
from mongoengine import *

class ModelOne(Document):
    int_value1 = IntField()
    int_value2 = IntField()
    boolean_value = BooleanField(required=True, default=False)

    @classmethod
    def get_model_one_by_value1(cls, v):
        return ModelOne.objects(int_value1=v)

    @classmethod
    def get_model_one_by_boolean_value(cls, v):
        return ModelOne.objects(boolean_value=v)

```


This is an example using the test nose + nose-mongoengine ( test_model_one.py )

``` python
# encoding:utf-8 #
from model_one import ModelOne
from nose.tools import assert_equals

class TestModelOne(object):

    # This method run on instance of class
    @classmethod
    def setUpClass(cls):

        global o1_id, o2_id

        # Create two objects for test
        o1 = ModelOne()
        o1.int_value1 = 500
        o1.int_value2 = 123
        o1.boolean_value = True
        o1.save()

        o2 = ModelOne()
        o2.int_value1 = 500
        o2.int_value2 = 900
        o2.boolean_value = False
        o2.save()

        # Save the id of objects to match in the test
        o1_id = o1.id
        o2_id = o2.id

    # This method run on every test
    def setUp(self):
        global o1_id, o2_id
        self.o1_id = o1_id
        self.o2_id = o2_id

    def test_match_with_value1(self):
        find = ModelOne.get_model_one_by_value1(500)
        assert_equals(len(find), 2)
        assert_equals(find[0].id, self.o1_id)
        assert_equals(find[1].id, self.o2_id)

    def test_match_with_boolean_value(self):
        find = ModelOne.get_model_one_by_boolean_value(True)
        assert_equals(len(find), 1)
        assert_equals(find[0].id, self.o1_id)

```

Run in the command line:

```

$ nosetests --mongoengine test_model_one.py 
..
----------------------------------------------------------------------
Ran 2 tests in 0.054s

OK

```

Todo
====

 - create automated tests
 - continuous integration with Travis ( http://travis-ci.org/ )

Authors
=======

Marcelo Anton ( https://github.com/mbanton/ )


Thanks to original author of mongonose: Kapil Thangavelu

