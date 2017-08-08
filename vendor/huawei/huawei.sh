#!/usr/bin/expect -f

# pymscoader the program for multiscript loader
# Copyright 2017 Ibrahim Khorwat
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
set username [lindex $argv 2]
set password [lindex $argv 3]
set enpasswd [lindex $argv 4]
set date [exec date +%F]
set sec [clock seconds]
set time [clock format $sec -format %H-%M-%S]

# This is a function to store log results into a certain file
proc loggit {hostname ip cause file} {
  log_file
  log_file -a $file
  set line "$hostname-$ip => $cause"
  send_error $line\n
  log_file
}

# Don't check keys
spawn ssh -o StrictHostKeyChecking=no $username\@$ip

# Please don't change the following timeout value
set timeout 5

# Create a history log file
log_file -a logs/history.log

expect {
timeout {
loggit $hostname $ip "Timeout Exceeded - please check ssh connectivity with the Host" "logs/failed.log"
exit 1 }
eof {
 loggit $hostname $ip "$expect_out(buffer)" "logs/failed.log"
 exit 1 }
"*assword" {
send "$password\r"
expect "*assword" {
  loggit $hostname $ip "The username or password is incorrect" "logs/failed.log"
  exit 1
}
}
}

log_file

# Log results are saved on the following directory
file mkdir logs/offlinecopies/$hostname-$ip
log_file -a logs/offlinecopies/$hostname-$ip/$hostname-$ip--$date--$time.log

# just to print a new line
send "\r"
expect ">"

# changing the default terminal lenght value from 24 to 0 so that show command
# doesn't display --More-- in the log files.
send "screen-length 0 temporary\r"
expect ">"


# Iterate over the configuraton commands to execute them one by one.
set f [open "./vendor/huawei/commands.txt"]
set cmds [split [read $f] "\n"]
close $f

# start sending the commands to the targeted device
foreach cmd $cmds {
  send "$cmd\r"
  expect "*#"
}

send "\n"
expect "*#"

loggit $hostname $ip "Successfully deployed the commands" "logs/history.log"

exit 1
