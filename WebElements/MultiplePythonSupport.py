"""
    MultiplePythonSupport.py

    Adds necessary hooks to allow python code to run on multiple major versions of python at once
    (currently 2.6 - 3.x)

    Usage:
        Anywhere you want to gain support for multiple versions of python add the following line
            from MultiplePythonSupport import *

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import sys

if sys.version > '3':
    long = int
    unicode = str

    def u(string):
        return string

    class dict(dict):
        def iteritems(self):
            return self.items()

        def itervalues(self):
            return self.values()

    from collections import OrderedDict

    class OrderedDict(OrderedDict):
        def iteritems(self):
            return self.items()

        def itervalues(self):
            return self.values()
else:
    try:
        from collections import OrderedDict
    except ImportError:
        from DictUtils import OrderedDict

    import codecs

    def u(string):
        return codecs.unicode_escape_decode(string)[0]
