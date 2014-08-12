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

from itertools import repeat,izip_longest
from math import trunc
from sys import stdout

def grid_lengths (grid):
    return map ( lambda row: map ( len, row), grid )


class Formater:
    """Class for applying a uniform alignment to different tables."""

    def __init__ (self, tabstop = 4):
        self.tabstop = tabstop
        self.widths = []


    def align (self, grid):
        # Save the length of the elements in the grid
        lengths = grid_lengths (grid)

        # Calculate the required length of the columns
        widths = map (max, zip(*lengths))

        # Fill the columns to the next tabstop
        widths = map (lambda width:
                        ( trunc (width/ self.tabstop) + 1) * self.tabstop,
                      widths)

        # Check whether or not the saved widths are larger and save the result
        self.widths = max (widths, self.widths)



    def format (self, grid):
        # Save the length of the elements in the grid
        lengths = grid_lengths (grid)

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
                    fill = self.widths[j] - lengths[i][j]
                    for _ in repeat (None, fill):
                        formated[i] += " "

        return formated



    def write (self, grid, writeable = stdout):
        formated = self.format (grid)

        for row in formated:
            writeable.write (row + '\n')



def write (grid, tabstop = 4, writeable = stdout):
    """A one shot formater."""
    formater = Formater (tabstop)
    formater.align (grid)
    formater.write (grid, writeable)

