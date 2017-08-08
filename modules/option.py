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

import getopt, sys
import os.path
from caller import isvalidip
from netaddr import IPNetwork
import shutil

def usage():
    print """
pymscoader v1.3
Usage: pymscoader [Options] [targets]
TARGETS:
  Can pass IP addresses and networks separated be spaces
  Ex: pymscoader 192.168.0.1 10.1.1.0/24 2001:db8:1::1
   If no targets have been specified, targets will be loaded from ip_list.txt
   file.
   If no targets are specified under the ip_list.txt file, the following message
   appear:
   [!] The (ip_list.txt) file should include at least one ip address.
  --exclude <host1[,host2][,host3],...>: Exclude hosts/networks separated by
  colons
OPTIONS:
  -h  --help            Show this help
  -n  --print-no-cmds   Don't Print out the commands that are going to be
                        executed (Disabled by Default)
  -V  --version         Displays the pymscoader verison
  -v  --verbose         activate verbose mode.
  -d  --default-vendor  Specify the default vendor name if no vendor name has
                        been typed before ip addresses in the ip_list.txt file
                        ex: 10.1.1.1
                            10.2.2.0/30
                        (The default vendorname =  cisco)
      --datetime        Spedify the date and time to schedual the execution of
                        the code the passed argument should be in the following
                        format YYYY.MM.DD_HH:MM:SS.
                        where <dot> separates the year from the month
                        from the day, <Underscrore> separates date from time,
                        <colon> separates hours from minutes from seconds.
                        You could use the following apscheduler cron-style
                        expressions if you want:
                        Expression |Field |	Description
                        --------------------------------------------------------
                        * 	        any    Fire on every value.
                        */a 	    any    Fire every a values, starting from
                                           the minimum.
                        a-b 	    any    Fire on any value within the a-b
                                           range (a must be smaller than b).
                        a-b/c 	    any    Fire every c values within the a-b
                                           range.
                        xth y 	    day    Fire on the x -th occurrence of
                                           weekday y within the month.
                        last x 	    day    Fire on the last occurrence of
                                           weekday x within the month.
                        last 	    day    Fire on the last day within the month
                        x,y,z 	    any    Fire on any matching expression; can
                                           combine any number of any of the
                                           above expressions.
                        --------------------------------------------------------
                        As example:
                        if you want the program to be executed every day if a
                        certain month at a certain time, simply type:
                        --datetime 2017.3.*_12:00:00
                        if you want the program to be executed every month at a
                        certain day and time, simply type:
                        --datetime 2017.*.1_12:00:00
                        and so on.
      --time            Specify the scheduled Time to run the script...
                        Time format is hh:mm:ss, you could also use cron-style
                        expressions mentinoed under the --datetime option.
                        This option is ment to be used in conjunciton with week
                        or day-of-week options, NOTE: if this option has been
                        chosen; it is going to override the time specified at
                        datetime option.
      --week            Specify the week number to execute the code
                        (from 1 to 53).
                        use --time option to set the time.
                        ( Note: If no time has been specified using --datetime
                        or --time option, the code will run at 12:00 AM at every
                        day during the specified week. )
      --day_of_week     number or name of weekday
                        (0-6 or mon,tue,wed,thu,fri,sat,sun) please use --time
                        option to set the time.
                        ( Note: If no time has been specified using datetime or
                        time options, the code will run at 12:00 O'clock AM at
                        the specified day. )
      --start-date      Specify the start date/time to execute the code.
                        ex:2017-03-23
                        or 2017-03-23T12:00:00
      --end-date        Specify the End date/time to execute the code.
                        ex:2017-03-23
                        or 2017-03-23T12:00:00
      --timezone        Specify the time zone to use for the date and time
                        calculation.
  -i  --ignore          Ignore changes done to the vendor scripts ( *.sh) by not
                        notifying the user about such changes.
                        example:
                        If the user choose -i option, he/she will not be
                        prompted to the below message
                        "
                        The file named as *.sh has been updated
                        Do you want to proceed [y/n]?
                        "
                        ( Recommended when Creating,Modifiying and/or testing
                        shell scripts under the vendor directory)
  -l  --login-cred      Get the login credential information
                        (username, password, and enable-passowrd) from the text
                        file named as cred_list.txt.
      --exclude         To exclude addresses or networks.
  -r  --rotate_limit    Limit the number of logs per device to not exceed the
                        specified number, the oldest log will be overwritten.
  -c  --clear_logs      Clear all logs under the logs directory including Device
                        logs under the offlinecopies directory.
  -s  --script          Enter the script name.
    """
    #TODO
    # - adding syslog messaging option
    # - adding email messaging option
    # - adding script option
    # - adding upload json file option ( to read the ip addresses instead of the built-in ip_list.txt file)

    exit()


def check_date_time(date_time):
        '''
        This function is to check the passed datetime so that it matches the format
        YYYY.MM.DD_HH:MM:SS
        This is to offer the user the ability to insert cron-style expression types
        like (*/a , a-b , a-b/c ...etc) without the need for --day , --month , --hour options
        example:
        >>>check_date_time('2017-9-9--11:11:11')
        [!] Error: The specified datetime doesn't match the format YYYY.MM.DD_HH:MM:SS
        >>>check_date_time('2017.9.9_11:11:11')
        >>>
        '''

        if date_time.count('.') == 2 and date_time.count(':') == 2 and date_time.count('_') == 1:
            date = date_time.split('_')[0]
            time = date_time.split('_')[1]
            year , month , day = date.split('.')[0] , date.split('.')[1] , date.split('.')[2]
            hour , minute , second = time.split(':')[0] , time.split(':')[1] , time.split(':')[2]
            return year , month , day ,  hour , minute , second
        print "[!] Error: The specified datetime doesn't match the format YYYY.MM.DD_HH:MM:SS "
        exit()


def read_passed_arguments(arguments):
    # getting the directoy where ip_list.txt file exists
    ip_list_dir = '/'.join(os.getcwd().split('/')) + '/ip_list.txt'
    subnets = []
    for item in arguments:
        # if the user inserts options after ip addresses the program will exit
        if '-' in item and len(item)>1:
            if item[1].isalpha():
                print 'Please make sure that options are passed before ip addresses'
                print 'example'
                print 'python pymscoader -v -i -n 10.1.1.1'
                print 'please type -h or --help for more information'
                exit()

        # if the user inserts colon between ip addresses
        elif ',' in item:
            print 'Please make sure no colons (,) are used in between addresses, use spaces instead.'
            print 'example:'
            print 'python pymscaoder 10.1.1.0/24 20.1.1.1'
            exit()
        # if valid ip addresses have been passed
        # UPDATE: It was
        #elif isvalidip(item):
        #    subnets.append(item)
        elif isvalidip(item.split('#')[0].strip()):
            subnets.append(item)
        elif not isvalidip(item) :
            print item,"<-please Enter a valid IP address"
            exit()
        else:
            usage()
    with open(ip_list_dir,'w') as fh:
        for ip in subnets:
            fh.write( ip + '\n')


def options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVvnd:ilr:ce:s:", ["help","version","verbose"\
                                               , "print-no-cmds","default-vendor=","datetime=","time="\
                                               , "week=","day-of-week=","start-date=","end-date=","timezone="\
                                               , "login-cred","ignore","exclude=","rotate_limit="\
                                               , "clear_logs","script="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    # Setting Default variables
    default_vendor = 'cisco'
    excluded_list = []
    year = month = week = day_of_week = day = hour = minute = second = start_date = end_date = timezone = None
    verbose = print_no_cmds = ignore = schedual = False
    script = email = login_cred = rotate_limit = None
    for o, a in opts:
        # reading user passed arguments
        if o in ("-h", "--help"):
            usage()
            exit()

        elif o in ("-V","--version"):
            print "Pymscoader verision 1.4"
            exit()

        elif o in ("-v","--verbose"):
            verbose = True
            print 'verbose has been activated'

        elif o in ("-n","--print-no-cmds"):
            print_no_cmds = True

        elif o in ("-d","--default-vendor"):
            if a in os.listdir('vendor'):
                default_vendor = a
            else:
                print "[!] Error: the specified vendor name",a,"is not currently supported"
                exit()

        elif o in ("--datetime"):
            year, month, day, hour, minute, second = check_date_time(a)
            print a,a.count('.')==2 and a.count(':')==2 and a.count('_')==1
            schedual = True

        elif o in ("--week"):
            schedual = True
            if a.isdigit() and int(a) in range(1,54):
                week = a
                # if no time has been set before; then set the time to 12:00 AM
                if hour == minute == second == None:
                    hour = '00' ; minute = '00' ; second = '00'

            else:
                print "[!] Error: the (week) argument must be an integer value between 1 and 53"
                exit()

        elif o in ("--day-of-week"):
            schedual = True
            # if no time has been set before; then set the time to be 12:00 AM
            if hour == minute == second == None:
                hour = '00' ; minute = '00' ; second = '00'

            if a.isdigit() and a in range(0,7):
                day_of_week = a

            elif a.isalpha() and a in ['mon','tue','wed','thu','fri','sat','sun']:
                day_of_week = a

            else:
                print "[!] Error: the (day-of-week) argument must be a number or name (0-6 or mon,tue,wed,thu,fri,sat,sun)"
                exit()

        elif o in ("--time"):
            if a.count(':') == 2:
                hour, minute, second = a.split(':')
                schedual = True

            else:
                print "[!] Error: the (time) argument must be in hh:mm:ss Format"
                exit()

        elif o in ("--start-date"):
            schedual = True
            start_date = a

        elif o in ("--end-date"):
            schedual = True
            end_date = a

        elif o in ("--timezone"):
            schedual = True
            timezone = a

        elif o in ("-i","--ignore"):
            ignore = True
            print "[+] The user choose to ignore changes done to the scriptS under vendor directory"

        elif o in ("--exclude"):
            for ip in a.split(','):
                if isvalidip(ip):
                    for execluded_ip in list(IPNetwork(ip)):
                        excluded_list.append(str(execluded_ip))
                else:
                    print '[!] Error: The execluded ip address',ip,'is not valid'
                    exit()

        elif o in ("-l","--login-cred"):
            login_cred = "cred_list.txt"
            print "[+] Credential information will be taken from",login_cred

        elif o in ("-r","--rotate_limit"):
            if a.isdigit():
                rotate_limit = a
                if rotate_limit == '0':
                    print "[!] Error: If you want to Delete all the logs please use -c or --clear_logs option"
                    exit()
                elif rotate_limit < '0':
                    print "[!] Error: rotate_limit option must be a positive integer number"
                    exit()

            else:
                print "[!] Error: rotate_limit option must be a positive integer number"
                exit()

            print "[+] log Rotation has been activated, number of logs per device is set to:",rotate_limit

        elif o in ("-c","--clear_logs"):
            print "[!] WARNING: All logs under the logs directory will be deleted"
            answer = raw_input('Would you like to proceed ?\n')
            while answer not in ['n','no','y','ye','yes']:
                print '\n[   please answer with n or y, no or yes    ] '
                answer=raw_input("Do you want to proceed [y/n]?\n")
            if answer in ["n","no"]:
                print "[+] No log have been deleted"
                exit()
            for i in os.listdir('logs'):
                try:
                    shutil.rmtree('logs/' + i)
                except:
                    os.remove('logs/' + i)
            print "[+] All logs under logs directory have been deleted"
            exit()

        elif o in ("-s","--script"):
            print a
            script = a

        #TODO
        #elif o in ("-e","--email"):
        #    email = a

        else:
            usage()

    if len(args) != 0:
        read_passed_arguments(args)

    if schedual:
        print '[+] schedualling has been activate'
        #if None not in [year , month , day, hour , minute , second]:
        #    print 'datetime:',datetime
        if year != None:
            print '    datetime: %s.%s.%s_%s:%s:%s'%(year,month,day,hour,minute,second)
        if week != None:
            print '    week:',week
        if day_of_week != None:
            print '    day-of-week:',day_of_week
        if start_date !=None:
            print '    start-date:',start_date
        if end_date != None:
            print '    end-date:',end_date
        if timezone != None:
            print '    timezone:',timezone

    print ""
    return verbose,print_no_cmds,default_vendor,year,month,day,week,day_of_week,hour,minute,second,\
    start_date,end_date,timezone,schedual,ignore,login_cred,excluded_list,rotate_limit,script


if __name__ == "__main__":
    options()
