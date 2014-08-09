#!/usr/bin/env python

# Small program for storing and retrieving paths from a database
# Copyright (C) 2014 Gustav Behm

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from os.path import expanduser, isfile
from os import getcwd
import anydbm
from optionparser import OptionParser, Command, Configuration
import sys


# Global configuration parameters
name = "qcd"
default_db_file = "~/." + name + "db"


# Wrappers for managing the database

def initialize_database (writeable = False):
    file = expanduser (file_option.value)

    if not writeable and not isfile(file):
        print >> sys.stderr, "Database is empty! Try adding something!"
        sys.exit (1)

    if writeable:
        return anydbm.open (file, 'c')
    else:
        return anydbm.open (file, 'r')

def close_database (db):
    db.close ()

# Helpers

def getAnonymousKey (db):
    i = 1;
    while True:
        if not str(i) in db:
            return str(i)
        i += 1

def syntaxError (info = ""):
    print >> sys.stderr, "Syntax error!" + info
    parser.usage ()
    sys.exit (2)



# Implementation of the commands

def add (args):
    if len (args) == 0 or len (args) > 2:
        syntaxError ()

    db = initialize_database (True)

    if len (args) == 2:
        key = args[0]
        db[key] = args[1]
    else:
        key = getAnonymousKey (db)
        db[key] = args[0]

    close_database (db)

def save (args):
    if len (args) > 1:
        syntaxError ()

    args.append ( getcwd() )
    add (args)

def change (args):
    if len (args) != 2:
        syntaxError ()

    db = initialize_database (True)

    if not args[0] in db:
        print >> sys.stderr, args[0] + " does not exist in the database."
        close_database (db)
        sys.exit (1)

    db[args[0]] = args[1]

    close_database (db)

def move(args):
    if len (args) != 2:
        syntaxError ()

    db = initialize_database (True)

    if not args[0] in db:
        print >> sys.stderr, args[0] + " does not exist in the database."
        close_database (db)
        sys.exit (1)

    if args[1] in db:
        print >> sys.stderr, args[1] + " already exist in the database."
        close_database (db)
        sys.exit (1)

    db[args[1]] = db[args[0]]

    del db[args[0]]

    close_database (db)

def delete (args):
    if len (args) != 1:
        syntaxError ()

    db = initialize_database (True)

    try:
        del db[args[0]]
    except:
        print >> sys.stderr, args[0] + " does not exist in the database."
        close_database (db)
        sys.exit (1)

    close_database (db)

def list (args):
    if len (args) != 0:
        syntaxError ()

    db = initialize_database ()
    for k, v in sorted (db.iteritems()):
        print >> sys.stderr, k + "\t" + v
    close_database (db)


def get (args):
    if len (args) != 1:
        syntaxError ()

    db = initialize_database ()

    try:
        print db[args[0]]
    except:
        print >> sys.stderr, args[0] + " does not exist in the database."
        close_database (db)
        sys.exit (1)

    close_database (db)


# The command line parser
parser = OptionParser (name)

# The options
file_option = Configuration ("f", "file", "Specifies which database to use", default_db_file)
parser.add (file_option)

# The commands
help_command = Command ("h", "help", "Prints this helpful message", lambda args:parser.usage ())
parser.add (help_command)

add_command = Command ("a", "add", "Add a new entry into the database", add)
parser.add (add_command)

save_command = Command ("s", "save", "Add current path into the database", save)
parser.add (save_command)

move_command = Command ("m", "move", "Rename an entry in the database", move)
parser.add (move_command)

change_command = Command ("c", "change", "Changes the path of an entry in the database", change)
parser.add (change_command)

delete_command = Command ("d", "delete", "Delete an entry from the database", delete)
parser.add (delete_command)

list_command = Command ("l", "list", "List the entries in the database", list)
parser.add (list_command)

retrieve_command = Command ("g", "get", "Retrieve an entry from the database", get, True)
parser.add (retrieve_command)


# Parse it!

parser.parse ()

