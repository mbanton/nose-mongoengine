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

Usage
=====

The plugin extends the nose options with a few options. The only
required options are either `--mongoengine` or `--mongoengine-mongodb-bin` to enable
the plugin.

 - `--mongoengine` is required to enable the plugin.

 - `--mongoengine-mongodb-bin` Allows specifying the path to the `mongod` binary.
   If not specified the plugin will search the path for a mongodb
   binary. If one is not found, an error will be raised.

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



Todo
====


Authors
=======

Marcelo Anton ( https://github.com/mbanton/ )


Thanks to original author of mongonose: Kapil Thangavelu

