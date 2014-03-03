#   Copyright 2012 Marcelo Anton
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
 nose plugin to facilitate the creation of automated tests that access Mongo
 Engine structures.
"""
import os
import shutil
import socket
import sys
import tempfile
import time
import uuid
import inspect
import subprocess

from subprocess import Popen
from nose.plugins import Plugin
from mongoengine.connection import connect


def scan_path(executable="mongod"):
    """Scan the path for a binary.
    """
    for path in os.environ.get("PATH", "").split(":"):
        path = os.path.abspath(path)
        executable_path = os.path.join(path, executable)
        if os.path.exists(executable_path):
            return executable_path


def get_open_port(host="localhost"):
    """Get an open port on the machine.
    """
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_sock.bind((host, 0))
    port = temp_sock.getsockname()[1]
    temp_sock.close()
    del temp_sock
    return port


class MongoEnginePlugin(Plugin):
    """A nose plugin to facilitate the creation of automated tests that access
       Mongo Engine structures.
    """

    def __init__(self):
        super(MongoEnginePlugin, self).__init__()
        self.mongodb_param = {}
        self.process = None
        self._running = False
        self.database_name = None
        self.connection = None
        self.clear_context = {}

    def options(self, parser, env=None):
        parser.add_option(
            "--mongoengine",
            action="store_true",
            default=False,
            help="Enable the mongoengine plugin.")

        parser.add_option(
            "--mongoengine-mongodb-bin",
            dest="mongodb_bin",
            action="store",
            default=None,
            help="Optionally specify the path to the mongod executable.")

        parser.add_option(
            "--mongoengine-clear-after-module",
            dest="mongoengine_clear_after_module",
            action="store_true",
            default=False,
            help="Optionally clear data in db after every module of tests.")

        parser.add_option(
            "--mongoengine-clear-after-class",
            dest="mongoengine_clear_after_class",
            action="store_true",
            default=False,
            help="Optionally clear data in db after every class of tests.")

        parser.add_option(
            "--mongoengine-mongodb-port",
            action="store",
            dest="mongodb_port",
            type="int",
            default=0,
            help="Optionally specify the port to run mongodb on.")
        parser.add_option(
            "--mongoengine-mongodb-scripting",
            action="store_true",
            dest="mongodb_scripting",
            default=False,
            help="Optionally enables mongodb script engine.")
        parser.add_option(
            "--mongoengine-mongodb-logpath",
            action="store",
            dest="mongodb_logpath",
            default="/dev/null",
            help=("Optionally store the mongodb "
                  "log here (default is /dev/null)"))
        parser.add_option(
            "--mongoengine-mongodb-prealloc",
            action="store_true",
            dest="mongodb_prealloc",
            default=False,
            help=("Optionally preallocate db files"))

    def configure(self, options, conf):
        """Parse the command line options and start an instance of mongodb
        """
        # This option has to be specified on the command line, to enable the
        # plugin.
        if not options.mongoengine or options.mongodb_bin:
            return

        if not options.mongodb_bin:
            self.mongodb_param['mongodb_bin'] = scan_path()
            if self.mongodb_param['mongodb_bin'] is None:
                raise AssertionError(
                    "Mongoengine plugin enabled, but no mongod on path, "
                    "please specify path to binary\n"
                    "ie. --mongoengine-mongodb=/path/to/mongod")
        else:
            self.mongodb_param['mongodb_bin'] = os.path.abspath(
                os.path.expanduser(os.path.expandvars(options.mongodb_bin)))
            if not os.path.exists(self.mongodb_param['mongodb_bin']):
                raise AssertionError(
                    "Invalid mongodb binary %r" % \
                    self.mongodb_param['mongodb_bin'])

        # Its necessary to enable in nose
        self.enabled = True

        db_log_path = os.path.expandvars(os.path.expanduser(
            options.mongodb_logpath))
        try:
            db_file = open(db_log_path, "w")
            db_file.close()
        except Exception as exc:
            raise AssertionError("Invalid log path %r" % exc)

        if not options.mongodb_port:
            self.mongodb_param['db_port'] = get_open_port()
        else:
            self.mongodb_param['db_port'] = options.mongodb_port

        db_prealloc = options.mongodb_prealloc
        db_scripting = options.mongodb_scripting

        self.clear_context['module'] = options.mongoengine_clear_after_module
        self.clear_context['class'] = options.mongoengine_clear_after_class

        # generate random database name
        self.database_name = str(uuid.uuid1())

        #########################################
        # Start a instance of mongo
        #########################################

        # Stores data here
        self.mongodb_param['db_path'] = tempfile.mkdtemp()
        if not os.path.exists(self.mongodb_param['db_path']):
            os.mkdir(self.mongodb_param['db_path'])

        args = [
            self.mongodb_param['mongodb_bin'],
            "--dbpath",
            self.mongodb_param['db_path'],
            "--port",
            str(self.mongodb_param['db_port']),
            # don't flood stdout, we're not reading it
            "--quiet",
            # save the port
            "--nohttpinterface",
            # disable unused.
            "--nounixsocket",
            # use a smaller default file size
            "--smallfiles",
            # journaling on by default in 2.0 and makes it to slow
            # for tests, can causes failures in jenkins
            "--nojournal",
            # Default is /dev/null
            "--logpath",
            db_log_path,
            "-vvvvv"
            ]

        if not db_prealloc:
            args.append("--noprealloc")

        if not db_scripting:
            args.append("--noscripting")

        self.process = Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )

        self._running = True
        os.environ["TEST_MONGODB"] = "localhost:%s" % \
                                     self.mongodb_param['db_port']
        os.environ["TEST_MONGODB_DATABASE"] = self.database_name

        # Give a moment for mongodb to finish coming up
        time.sleep(0.3)

        # Connecting using mongoengine
        self.connection = connect(self.database_name, host="localhost",
                port=self.mongodb_param['db_port'])

    def stopContext(self, context):
        """Clear the database if so configured for this
        """

        # Use pymongo directly to drop all collections of created db
        if ((self.clear_context['module'] and inspect.ismodule(context)) or
           (self.clear_context['class'] and inspect.isclass(context))):
            self.connection.drop_database(self.database_name)

    def finalize(self, result):
        """Stop the mongodb instance.
        """

        if not self._running:
            return

        # Clear out the env variable.
        del os.environ["TEST_MONGODB"]
        del os.environ["TEST_MONGODB_DATABASE"]

        # Kill the mongod process
        if sys.platform == 'darwin':
            self.process.kill()
        else:
            self.process.terminate()
        self.process.wait()

        # Clean out the test data.
        shutil.rmtree(self.mongodb_param['db_path'])
        self._running = False
