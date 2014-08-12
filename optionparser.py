#!/usr/bin/env python

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

"""An abstraction layer wrapping the parsing of command line options."""

__author__ = "Gustav Behm"
__copyright__ = "Copyright 2014, Gustav Behm"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import getopt
import inspect
import sys

import tabularize

class Option:
    """The base class for an option"""

    def __init__ (self, short_name, long_name, description, syntax = ""):
        """The constructor: specify names, short and long, and a description of the option."""
        self.option = short_name
        self.long_option = long_name
        self.description = description
        self.syntax = syntax



    def describe (self):
        """Method for making the option describe itself"""
        columns = []

        if len (self.syntax) > 0:
            columns.append ("-" + self.option + ", --" + self.long_option + ":")
            columns.append ("-" + self.option + " " + self.syntax)
        else:
            columns.append ("-" + self.option + ", --" + self.long_option)
            columns.append ("")

        columns.append (self.description)
        return columns

    def __eq__ (self, other):
        """Overloaded comparison with a string. Will compare for -short_name and --long_name"""
        if type(other) is str:
            return (other == "-" + self.option) or (other == "--" + self.long_option)
        else:
            return NotImplemented

    def makeOptString (self):
        return self.option

    def makeLongOptString (self):
        return self.long_option

    def do (self, args):
        """Unimplemented for handling the actions called for by the option"""
        return NotImplemented



class Command(Option):
    """An option which when set calls the callback provided."""

    def __init__ (self, option, long_option, description, callback, is_default = False, syntax = ""):
        """Contructor asking for names, description and a callback"""
        Option.__init__ (self, option, long_option, description, syntax)
        self.callback = callback
        self.is_default = is_default

    def do (self, args):
        """This will call the callback"""
        self.callback (args)


class Configuration(Option):
    """An option which stores the parameter passed on the command line"""

    def __init__ (self, option, long_option, description, default, syntax = ""):
        """Contructor asking for names, description and the default (and initial) value of this option"""
        Option.__init__ (self, option, long_option, description, syntax)
        self.value = default

    def do (self, arg):
        """This will store the parameter in the value attribute"""
        self.value = arg

    def makeOptString (self):
        return self.option + ":"

    def makeLongOptString (self):
        return self.long_option + "="




class OptionParser:
    """The object abstracting the command line parsing using Option objects"""

    def __init__ (self, name):
        """The constructor which asks only for the name of the application"""
        self.options = []
        self.name = name

    def add (self, option):
        """Add an option to be parsed."""
        self.options.append (option)

    def has (self, query):
        """Internal method for querying what we have in the options list"""
        if inspect.isclass(query):
            for o in self.options:
                if isinstance(o, query):
                    return True
            return False
        else:
            return query in self.options

    def usage (self):
        """Compile and print the usage information"""

        # Initiaize the formater
        tabstop = 4
        formater = tabularize.Formater (tabstop)

        # Obtain the config options and align the formater
        configs = []
        for o in self.options:
            if isinstance (o, Configuration):
                configs.append(o.describe ())
        formater.align (configs)

        # Obtain the commands and align the formater
        commands = []
        for o in self.options:
            if isinstance (o, Command):
                commands.append  (o.describe ())
        formater.align (commands)

        # Start writing the usage line
        usage_line = "Usage: " + self.name

        if len (configs) > 0:
            usage_line += " [OPTIONS]..."

        if len (commands) > 0:
            usage_line += " [COMMANDS]..."

        print >> sys.stderr, usage_line

        # Write the configs
        if len (configs) > 0:
            print >> sys.stderr, "\nConfiguration options:"
            formater.write (configs, writeable = sys.stderr)

        # Write the commands
        if self.has (Command):
            print >> sys.stderr, "\nAvailable commands:"
            formater.write (commands, writeable = sys.stderr)

    def parse (self):
        """Do the parsing of arguments passed on the command line"""
        optstr = ""
        longopts = []

        # Complie the arguments for getopt
        for o in self.options:
            optstr += o.makeOptString ()
            longopts.append (o.makeLongOptString ())


        # Parse the command line with getopt
        try:
            opts, remaining = getopt.getopt (sys.argv[1:], optstr, longopts)
        except getopt.GetoptError as err:
            # Handle a syntax error
            print >> sys.stderr, str (err)
            self.usage ()
            sys.exit (2)

        # Configure all the configuration options
        for o, a in opts:
            for opt in self.options:
                if isinstance (opt, Configuration) and o == opt:
                    opt.do (a)
                    break

        # Look for a command and do it if we find it
        for o, a in opts:
            for opt in self.options:
                if isinstance (opt, Command) and o == opt:
                    opt.do (remaining)
                    return

        # No command was found, hence we look for a default command
        for opt in self.options:
            if isinstance (opt, Command) and opt.is_default:
                opt.do (remaining)
                return

        # No default command, we don't know what to do!

        print >> sys.stderr, "No command was specified."
        self.usage ()
        sys.exit (2)





