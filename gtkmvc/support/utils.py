#  Author: Roberto Cavada <cavada@fbk.eu>
#
#  Copyright (c) 2007 by Roberto Cavada
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



def get_function_from_source(source):
    """Given source code of a function, a function object is
    returned"""

    import re
    m = re.compile("def\s+(\w+)\s*\(.*\):").match(source)
    if m is None: raise ValueError("Given source is not a valid function:\n"+
                                   source)
    name = m.group(1)
    
    exec source
    code = eval("%s.func_code" % name)
    import new
    return new.function(code, globals(), name)    
