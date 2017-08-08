# pymscoader the program for multiscript loader
# Copyright 2017 Ibrahim Abdulghni Khorwat
# This file is part of pymscoader.
#
# pymscoader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pymscoader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pymscoader.  If not, see <http://www.gnu.org/licenses/>.
import os

def log(*args):
    '''
    This is to print out the logs and write them down to the history.txt file
    '''
    line = ' '.join( str(arg) for arg in args )
    print line
    if not os.path.exists( 'logs' ):
        os.mkdir('logs')
    with open('logs/history.log','a+') as fh:
        fh.write(line+'\n')
