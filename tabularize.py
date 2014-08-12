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

"""Simple helpers for tabularizing a grid."""

__author__ = "Gustav Behm"
__copyright__ = "Copyright 2014, Gustav Behm"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

from itertools import repeat
from math import trunc
from sys import stdout

def format (grid, tabstop = 4):
    # Save the length of the elements in the grid
    lengths = map ( lambda row: map ( len, row), grid )

    # Calculate the required length of the columns
    widths = map (max, zip(*lengths))

    # Fill the columns to the next tabstop
    widths = map (lambda width: ( trunc (width/tabstop) + 1) * tabstop, widths)

    # Iterate through the grid and make formated rows
    formated = []
    for i, row in enumerate (grid):
        formated.insert(i, "")
        row_length = len (row) - 1 # Minus one since the lists are zero-indexed
        for j, element in enumerate (row):
            # Add the element...
            formated[i] += element

            # ... and if we are not at the last column...
            if j < row_length:
                # ... then we fill the rest with spaces
                fill = widths[j] - lengths[i][j]
                for _ in repeat (None, fill):
                    formated[i] += " "

    return formated

def write (grid, tabstop = 4, writeable = stdout):
    formated = format (grid, tabstop)

    for row in formated:
        writeable.write (row + '\n')

