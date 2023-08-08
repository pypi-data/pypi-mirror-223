# -*- coding: utf-8 -*-

# Microlib is a small collection of useful tools.
# Copyright 2020 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Microlib.

# Microlib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Microlib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Microlib; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
from pathlib import Path

import toml

from . import terminal, database
from .xdict import XDict
from .tools import rotate, grouper, read_text, fracdigits_nb, turn_to_capwords
from .configfile import StandardConfigFile
from .deprecation import Deprecated

pp = Path(__file__).parent / 'data/pyproject.toml'
__version__ = toml.loads(pp.read_text())['tool']['poetry']['version']

__all__ = [terminal, XDict, rotate, grouper, read_text, StandardConfigFile,
           database, fracdigits_nb, turn_to_capwords, Deprecated]
