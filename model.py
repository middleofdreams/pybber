#  Author: Roberto Cavada <cavada@fbk.eu>
#
#  Copyright (c) 2006 by Roberto Cavada
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


import _importer
from gtkmvc import Model
from connection_model import *

class MyModel (Model):
    """Our model contains a numeric counter and a numeric value that
    holds the value that the counter must be assigned to when we the
    model is reset"""
    
    counter = 0
    reset_value = 0

    __observables__ = ('counter', 'reset_value')
    

    def __init__(self):
        Model.__init__(self)
        self.connection=ConnectionModel()
        self.observe_model(self.connection)
        return

    def reset(self): self.counter = self.reset_value

    pass # end of class
    
