Description:
===================
pymscoder is a python_2.7 program for loading a script and running it into multithreaded processes.
This program was mainly used to gather the output of multiple show commands from multiple cisco devices or to deploy multiple cisco configuration commands on multiple cisco devices without the need to manually log into each device and type every individual command many times, but this program could also be used to gather or deploy other vendor commands if you have its shell script available.

Althogh similar features Plus more already exists on an open source project called ( Ansible )
But it is greate to challenge my self to build simlar software program using python.

author name : Ibrahim Abdulghni Khorwat

Files and Directories:
=====================
    - modules: All required python modules are stored on "modules" folder.

    - GNS3-TEST: This folder contains a ready network for testing the pymscoader program, you might need to read the "copypast.txt" to simply copy and past it into your local machine to have the related tap0 ready and set.

    - ip_list.txt: This file includes the targetted ip addresses you want the program to log into them.

    - cred_list.txt: This file inculdes the username, password and enable password, this is optional if you want the program to automatically log into devices without asking for user credentails at the very beginning. to activate this option simply type:

user@user:~$python pymscoader.py -l cred_list.txt

Note:

Currently the pymscoader supports Only One login Password for all Devices.


    - vendor: is a directory that holds the script of the currently supported vendors (cisco,huawei,alcatel,mikrotick and linux)

    - /vendor/cisco: This folder contains the shell scripts for executing show commands or configuration commands, it also contains the commands to be executed either for show or for configuraiton. as example:

"cisco.sh" is a linux shell script that loads cisco commands from "commands.txt" file

Once you execute pymscoader; a new files will be created on the same directory, these files are:

    - md5_cache.txt: This file stores the md5 hash of the loaded shell script, so that it will warn you if there are any changes done to the loaded shell script.

    - history.log: You could consider this file as a log file that shows the establishment of ssh connection with the targeted devices, every time you execute the program new logs will be appended.

- failed.log: If the program failed to access any targeted devices shell it will be logged into this file, devices are logged here due to one of the following reasons:

 * Timeout or the devices is busy.
 
 * Device is unreachable.
 
 * SSH port is closed.
 
 * username or password is incorrect.
 
 * enable password is incorrect.


Important
=========
- capable host machines

This program has been tested only on Linux, and its related distribution.

- Python version
2.7

- You might need to allow the shell scripts to be executable by doing the below command:

user@user:~$sudo chmod a+x cisco_config.sh

user@user:~$sudo chmod a+x cisco_show.sh

- You need to have expect already installed

user@user:~$sudo apt-get install expect

- You need to Download and install python netaddr module

user@user:~$easy_install netaddreasy_install netaddr


How To Use:
==========

The default loaded script is "cisco_show.sh" which is a an expect shell script for running multiple show commands found on "show_cmds.txt" on multiple cisco devices specified in the ip_list.txt file. this script can be found under "cisco" directory.

To run the default script "cisco_show.sh" simply type:

user@user:~$python pymscoader

The script will ask you to enter the username, the password and the enable password (if avilable - you could just type Enter if there is no enable passsowrd), then it will read the ip_list.txt file loading all available ip addresses ( which can be written as a subnet ex: 10.0.0.0/24 or just as an ip address 10.0.0.1) and read all the show commands found on "show_cmds.txt" file, then it will ssh into all of the targeted devices (ip addresses) and excute the commands one by one, there is a certain time delay between every two commands in order not to overload the CPU with requests, the result will be stored on a directory called offlinecopies, if you go into this directory you will find as much files as the number of successfully logged-in devices, here is a tree view of what you would see if the program managed to access these ip addresses (10.1.1.1, 192.168.1.2, 172.16.5.5)

offlinecopies
|
-- 10.1.1.1
| |
| |__offlinecopy-10.1.1.1-2016-12-1-12-00-00.log

| |__offlinecopy-10.1.1.1-2016-12-1-13-00-00.log
|
-- 172.16.5.5
| |
| |__offlinecopy-172.16.5.5-2016-12-1-12-00-00.log

| |__offlinecopy-172.16.5.5-2016-12-1-13-00-00.log
|
-- 192.168.1.2
  |
  |__offlinecopy-192.168.1.2-2016-12-1-12-00-00.log
  
  |__offlinecopy-192.168.1.2-2016-12-1-13-00-00.log

You could notice the time of the log at the last of the file name (12-00-00 means 12:00:00).
If the program couldn't access the devices for reachability issue or for user credential issue, you will not find any file created, instead you will find the ip addresses logged into the failed.log file.
if the shell script has been modified for any reason, the next time you run the program you will be asked whether you will need to proceed runnign the program or not, this is just for security reason and that you are really aware of any changes. If you don't want to be questioned every time you do changes to the shell script you could simply type:

user@user:~$python pymscoader -i

or

user@user:~$python pymscoader --ignore

If you want to run multiple configuration commands on multiple cisco devices, you need to load another script which is named as: "cisco_config.sh", you will need to simply type:

user@user:~$python pymscoader -s cisco_config.sh
or
user@user:~$python pymscoader --script cisco_config.sh

The result will be stored on a directory called "deployedcopies",if you go into this directory you will find as much files as the number of successfully logged-in devices, here is a tree view of what you would see if the program managed to access these ip addresses (10.1.1.1, 192.168.1.2, 172.16.5.5)

deployedcopies
|
-- 10.1.1.1
| |
| |__deployedcopy-10.1.1.1-2016-12-1-12-00-00.log

| |__deployedcopy-10.1.1.1-2016-12-2-12-00-00.log
|
-- 172.16.5.5
| |
| |__deployedcopy-172.16.5.5-2016-12-1-12-00-00.log

| |__deployedcopy-172.16.5.5-2016-12-2-12-00-00.log
|
-- 192.168.1.2
  |
  |__deployedcopy-192.168.1.2-2016-12-1-12-00-00.log
  
  |__deployedcopy-192.168.1.2-2016-12-2-12-00-00.log


How To Do Schedualling
======================

you have these options

-Y --year

-M --month

-W --week

-D --Day

-H --hour

-M --minute

-S --second

so if you want to run the show commands every 5 hours, you simple type

user@user:~$python pymscoader -H 5

or

user@user:~$python pymscoader --hour 5


How To Create another Vendor shell script
========================================

You just create another directory - within this program direcoty - with a vendor name.

example:

if the vendor is Huawei create a directory called huawei

if the vendor is Avaya create a directory called avaya

This directory should include the shell script and the commands to be loaded by this scipt.

as example: To run huawei display commands using the shell script "huawei_display.sh" through pymscoader simply type:

user@user:~$python pymscoader -v hauwei -s huawei_display.sh


changing the ip addresses in the ip_list.txt file will not take affect if schedualling has been activated until you deactivate then activate the pymscoader again, technically it is possible to do this, and i had two options, either to add a global variable under the launch function which i don't like to do (staying a way from Global varibale), or make the schedualling under the main loop which forms a design issue in my prospective.

Scheduling
----------
yearly, monthly,weekly,daily, hourly,m,se

if the script to be run every year at a certain day
--datetime *.1.1_00:00:00

if the script to be run on  acertain day and every month within a year
--datetime 2017.*.1_00:00:00

if the script to be run every day within a year
--datetime 2017.*.*_00:00:00

if the script to be run every day within a month of a year
--datetime 2017.1.*_00:00:00

if the script to be run every day during a certain week use, Note the default time is set to be 12:00 AM, if you want to change this time use --time option.
--week 13 --time 00:00:00

if the script to be run weekly and at a certain day
--day-of-week sat
or
--day-of-week 0



Still under Develpoment
=======================
Support other host machines other than linux.

Support python 3 version of this program.

Creating other vendor shell scripts.

Sending a Notification by email if the program has been completed its [ schedualled ] process.

