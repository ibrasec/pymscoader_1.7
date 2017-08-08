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

import getpass

def get_user_credentials(login_cred):
    if login_cred != None:
        with open(login_cred) as fh:
            cred_list=fh.readlines()
            if len(cred_list)<9:
                cred_list.append('')
            username,password,enpasswd=cred_list[4].strip(),cred_list[6].strip(),cred_list[8].strip()
            return username,password,enpasswd
    else:
        try:
            username=raw_input("Please Enter the username:\n")
            while username=='':
                username=raw_input("[!] The username must not be empty. \nPlease Enter the username:\n")
            password=getpass.getpass("Please Enter the Password:\n")
            enpasswd=getpass.getpass("Please Enter the Enable password if configued otherwise press Enter:\n")
            return username,password,enpasswd
        except KeyboardInterrupt:
                print 'Exiting the Program'
                exit()


if __name__=='__main__':
    get_user_credentials()
