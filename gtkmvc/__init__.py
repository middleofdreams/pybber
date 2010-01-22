#  Author: Roberto Cavada <cavada@fbk.eu>
#
#  Copyright (c) 2005 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.


__all__ = ["model", "view", "controller", "observable", "observer", "support"]

__version = (1,99,0)

from model import Model, TreeStoreModel, ListStoreModel, TextBufferModel
from model_mt import ModelMT
from controller import Controller
from view import View
from observer import Observer
import observer
import observable
import adapters

def get_version(): return __version

def require(ver):
    if isinstance(ver, str): ver = ver.split(".")
    ver = tuple(map(int, ver))
    
    if get_version() < ver:
        raise AssertionError("gtkmvc required version '%s', found '%s'"\
                             % (ver, get_version()))
        pass
    return


