# -*- coding: utf-8 -*-
#########################################################################
# Copyright (C) 2014 by Simone Gaiarin <simgunz@gmail.com>              #
#                                                                       #
# This program is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

"""
Entry point for Fluent Forever Vocabulary Deck Builder add-on for Anki
"""

import os, sys

#Add folder extmodules to path in order to provide all the required libraries
rootPath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(rootPath, 'ffvocdeckbuilder', 'extmodules'))

import ffvocdeckbuilder.ffvocdeckbuilder
