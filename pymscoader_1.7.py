#!/usr/bin/python

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

import threading
import time
import os
import signal
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from colorama import init, Fore
from netaddr import IPNetwork
from modules.caller import call_targets
from modules.log_limiter import limit_logs
from modules.mini_logger import log
from modules.option import options
from modules.ask.credentials import get_user_credentials
from modules.ask.script_changed import script_changed
import logging,six
import sqlite3

logging.basicConfig()

# Creating a Database if No Database exists
conn = sqlite3.connect('DevicesStatus.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS DEVICES;")
cur.execute("CREATE TABLE IF NOT EXISTS DEVICES \
(Link_ID  INTEGER  PRIMARY KEY AUTOINCREMENT, Vendor NVARCHAR (40), Hostname NVARCHAR (40), Ip TEXT, Status   NVARCHAR (40),  Comments TEXT)")


# setting the color back to white
init(autoreset=True)
# for scheduling
running = True

# defining Enterrupt function
def signal_handler(signal, frame):
    print '\n'
    exit()


# loading passed options
( verbose , print_no_cmds , default_vendor,\
Year , Month , Day , Week , Day_of_week , Hour , Minute , Second,\
Start_date , End_date , Timezone , schedual , ignore , login_cred , excluded_list , rotate_limit ,script ) = options()


# Reading the ip_list.txt file
target_list = call_targets( excluded_list , default_vendor )

# definining print out command funciton (optional)
def printout_cmds():
    """
    This is to display the commands that are going to be executed for each
    selected vendor, as an example: if the user specified cisco and huawei
    as vendors in the ip_list.txt file, the commands.txt files under both
    /vendor/cisco/ and vendor/huawei directories are going to be displayed.
    """
    v = []
    for target in target_list:
        if target[0] not in v:
            v.append( target[0] )
            vendor_commands =  'vendor/' + target[0] + '/' + 'commands.txt'
            log("The following commands are going to be executed for <",target[0],"> Devices:")
            log("#"*80)
            with open (vendor_commands) as fh:
                cmds = fh.readlines()
                for cmd in cmds:
                    log(cmd.strip())
            log("#"*80)

# To print out the commands that are going to be executed
if not print_no_cmds:
    printout_cmds()


# verifying that no changes have been done to the scripts.
# this is just to give some warning for any unexpectedly done overwritten

vendors = os.listdir('vendor')
if ignore == False and script == None:
    for vendor in vendors:
        # example: vendor/cisco/cisco.sh
        script_directory = 'vendor/' + vendor + '/' + vendor + '.sh'
        try:
            script_changed(script_directory)
        except KeyboardInterrupt:
                print 'Exiting the Program'
                exit()


# the main thread class
class Connect(threading.Thread):
    """
    Multithreading
    The shell script is specified under the (run) method.
    """

    def __init__( self, threadID , vendor , host , ip , port ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.vendor = vendor.strip()
        self.host = host.strip()
        self.ip = ip.strip()
        self.port = port.strip()

    def run(self):
        """
        Thread run method. execute the shell script on the targeted ip address.
        """
        if script != None:
            cmd = 'python ' + script + ' ' + self.ip
        # example: vendor/cisco/cisco.sh
        else:
            vendor_directory = self.vendor + '/' + self.vendor + '.sh'
            cmd = 'vendor/' + vendor_directory + ' ' + self.host   + \
                                                 ' ' + self.ip  + \
                                                 ' ' + self.port  + \
                                                 ' ' + username + \
                                                 ' ' + password + \
                                                 ' ' + enpasswd + " > /dev/null"
        if verbose:
            print(Fore.GREEN + "[ + ] processing " + self.ip + " port " + self.port + " => Assigned to thread-id " + str(self.threadID))

        os.system(cmd)
        if verbose:
            print(Fore.YELLOW + "[ . ] End processing "+ self.ip + " at " + time.ctime() )


# getting user credentials
username,password,enpasswd = get_user_credentials(login_cred)


# Defining the main function
def launch():
    """
    This is where the program assigns an ip address to each working thread,
    the number of working threads is equal to the number of ip addresses
    specified at the < ip_list.txt > file
    """
    port = '22'
    log("="*80,"\nStarting New launch ---->-----  ", time.ctime(),"\n" )
    with open('logs/failed.log','w') as fh:
            fh.write("="*80+"\n"+' --- New list of failed to process ip addresses ---' + time.ctime() + "\n")
    thread_id = 0
    for target in target_list:
        vendor,hostname,ip_= target[0],target[1],target[2]
        if '#' in ip_:
            ip = ip_.split('#')[0].strip()
            port_ = ip_.split('#')[1].strip()
            if port_.isdigit() and port_ != '':
                port = str(port_)

        t = Connect( thread_id , vendor , hostname , ip , port )
        t.start()
        time.sleep(.005)
        thread_id+= 1
    # checking if schedualling option has been selected.
    # wait untill all threads finsh their jobs
    if schedual:
        while threading.activeCount() != 3:
            time.sleep(1)

    else:
        while threading.activeCount() != 1:
            time.sleep(1)
    # To apply log rotation after all threads are finished.
    limit_logs( rotate_limit )
    if schedual:
        sched.print_jobs()

#-------------------------------------------------
if __name__ == '__main__':
    if schedual:
        print 'Waiting for the scheduled time ...'
        try:
            sched = BackgroundScheduler()
            sched.add_job(launch, 'cron',year=Year,month=Month,week=Week,day=Day,\
            day_of_week=Day_of_week,hour=Hour,minute=Minute, second= Second,\
            start_date=Start_date,end_date=End_date,timezone=Timezone)
            sched.start()

            while running:
                time.sleep(1)
                #print 'active under',threading.activeCount()
                # To close the apscheduler once all jobs have been done
                for s in sorted(six.iteritems(sched._jobstores)):
                    jobs = s[1].get_all_jobs()
                    if jobs ==[]:
                        running = False
                        print 'Processing the last job...'

        except (KeyboardInterrupt, SystemExit):
            print '\nThe program has been interrupted'
            sched.shutdown()
            conn.commit()
            exit()

        while threading.activeCount() not in [3,4]:
            signal.signal(signal.SIGINT, signal_handler)
            time.sleep(1)

        print "All scheduled jobs have been finshed"

    else:
        signal.signal(signal.SIGINT, signal_handler)
        conn.commit()
        launch()

    conn.commit()
    exit()
