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

def remove_logs( path , amount ):
    '''
    This function is used to remove the amount of logs specified by the passed
    (amount) variable.
    The oldest logs are going to be removed
    '''
    logs = os.listdir( path )
    # keep removing logs until we got the same number of limitted logs
    for i in range( amount ):
        # To remove the oldest log
        old_log = path + '/' + min(logs)
        os.remove( old_log )
        print min(logs)," >>> Deleted: limit logs exceeded"
        logs.remove( min(logs) )


def limit_logs( limit = None ):
    '''
    This function is used to call remove_logs function if the (offlinecopies)
    directory exists and the number of limited logs is less than what each
    sub-directories contains.
    '''
    if os.path.exists( 'logs/offlinecopies' ) and limit != None and limit > 0:
        sub_dirs = os.listdir( 'logs/offlinecopies' )
        for each_dir in sub_dirs:
            # calculating number of logs per each sub-directory
            path = 'logs/offlinecopies/' + each_dir
            #print path
            count_logs = len( os.listdir( path ) )
            if count_logs > int(limit):
                # leave the following number of logs
                amount = count_logs - int(limit)
                remove_logs( path , amount )
    else:
        # if no logs has been saved yet.
        pass


if __name__ == '__main__':
    limit_logs()
