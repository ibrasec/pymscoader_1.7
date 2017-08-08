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

import hashlib
import sys
import os


def checkmd5(shell_script):
    """
    This is to return the md5 hash of the passed shell script
    """
    hash_md5 = hashlib.md5()
    with open(shell_script, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def learn_md5(shell_script):
    """
    This is to save the name of the passed shell script and its md5 hash
    into the md5_cache.txt file.
    ex:
    vendor/cisco/cisco.sh 27d9b397dfbe26ffeaa18b145829c5e2
    vendor/huawei/huawei.sh ab916a07f06e3ea206b0bde92926c542
    """
    with open("md5_cache.txt","a") as f:
        line = shell_script + ' ' + checkmd5(shell_script) + '\n'
        f.write(line)


def update_md5(shell_script):
    """
    This is to update the md5 hash of the passed shell_script
    and overwrite its previouse value stored on the md5_cache.txt file.
    """
    with open("md5_cache.txt","r") as f:
        list = f.readlines()
    for line in list:
        if shell_script in line:
            md5_result = checkmd5(shell_script)
            list[list.index(line)] = shell_script + ' ' + md5_result + '\n'
            with open("md5_cache.txt","w") as f:
                for line in list:
                    f.write(line)


def script_isloaded(shell_script):
    """
    This is to check if the passed shell_script is already included
    in the md5_cache.txt file.
    """
    with open("md5_cache.txt","a+") as f:
        md5_cache=f.readlines()
    for script in md5_cache:
        if shell_script in script:
            return True
    return False


def call_md5(shell_script):
    """
    This is to return the md5 hash of the passed shell_script located
    in the md5_cach.txt file.
    """
    with open("md5_cache.txt","r") as f:
        md5_cache=f.readlines()
    for line in md5_cache:
        if shell_script in line:
            return line.split()[1]


def script_changed(shell_script):
    """
    Based on the above functions, this function creates or updates the md5-hash of the
    passed shell script. Since this module is located on a different directory,
    the passed shell_script should be in the following format:
    vendor/<vendor-name>/<script-name>
    example:
    vendor/cisco/cisco.sh
    """
    # To check if the md5 hash of the shell_script exists in the md5_cache.txt file
    if not script_isloaded(shell_script):
        learn_md5(shell_script)
    else:
        # To check if the md5 hash of the passed shell_script matches the existing one.
        if checkmd5(shell_script) != call_md5(shell_script):
            print ""
            print "[!] Warning"
            print "The file named as",shell_script,"has been updated"
            answer=raw_input("Do you want to proceed [y/n]?\n")
            while answer not in ['n','no','y','ye','yes']:
                print '\n[   please answer with n or y, no or yes    ] '
                answer=raw_input("Do you want to proceed [y/n]?\n")
            if answer in ["n","no"]:
                print "The Program is going to exit"
                exit()
            else:
                answer=raw_input("Do you want me to learn its md5 hash? [y/n]\n")
                while answer not in ['n','no','y','ye','yes']:
                    print '\n[   please answer with n or y, no or yes    ] '
                    answer=raw_input("Do you want me to learn its md5 hash[y/n]?\n")
                if answer in ["y","ye","yes"]:
                    update_md5(shell_script)


if __name__ == '__main__':
    script_changed(sys.argv[1])
