#!/usr/bin/expect -f

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

# Setting variables
set hostname [lindex $argv 0]
set ip [lindex $argv 1]
set ssh_port [lindex $argv 2]

# +c80w is appended to the username in order to disable console colors
# and to set the terminal width to 80 the width as 80 as mentioned in the
# below link
# https://wiki.mikrotik.com/wiki/Manual:Console_login_process
set username "[lindex $argv 3 ]+c80w"
set password [lindex $argv 4]
set date [exec date +%F]
set sec [clock seconds]
set time [clock format $sec -format %H-%M-%S]



file mkdir logs/offlinecopies/$hostname-$ip
set log_directory "logs/offlinecopies/$hostname-$ip/$hostname-$ip--$date--$time.log"


# This is a function to store log results into a certain file
proc loggit {hostname ip cause file} {
  log_file
  log_file -a $file
  set line "$hostname > $ip >> $cause"
  send_error $line\n
  log_file
}

# Don't check keys
spawn ssh -o StrictHostKeyChecking=no $username\@$ip -p $ssh_port


# Please don't change the following timeout value
set timeout 10

# Create a history log file
log_file -a logs/history.log


expect {
timeout {
loggit $hostname $ip "Timeout Exceeded " "logs/failed.log"
exit 1
}
eof {
loggit $hostname $ip "$expect_out(buffer)" "logs/failed.log"
 exit 1
}
"*assword" {
send "$password\r"
expect "Access denied" {
  loggit $hostname $ip "The username or password is incorrect" "logs/failed.log"
  exit 1
}
}
".*" {
  send "\r\n"
  expect "..*"
}
}

# closing the previous log file.
log_file


# just to print a new line
send "\n\r"
expect "..*"


set timeout 10


for {set id 2} {$id < 254} {incr id 1} {
send "/interface bridge add name=loopback$id\r"
expect "*>"
send "/interface bridge\r"
send "/ip address add  address 1.1.1.$id/32 interface loopback$id\r"
sleep 0.25
}




loggit $hostname $ip "Successfully deployed the commands" "logs/history.log"

exit 1
