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
set username [lindex $argv 3]
set password [lindex $argv 4]
set enpasswd [lindex $argv 5]
set date [exec date +%F]
set sec [clock seconds]
set time [clock format $sec -format %H-%M-%S]

#setting the colors
set normal "\033\[0;0m"
set green "\033\[32m"
set red "\033\[1;31m"

# settting show options
set sh "sh"
set show "show"
set do_sh "do sh"
set do_show "do show"

set vendor "cisco"

# This is a function to store log results into a certain file
proc loggit {hostname ip cause file} {
  log_file
  log_file -a $file
  set line "$hostname > $ip >> $cause"
  send_error $line\n
  log_file
}

proc send_sql {vendor hostname ip status date time sec} {
  log_file
  spawn sqlite3 DevicesStatus.sqlite
  expect "sqlite"
  send "insert into DEVICES (Vendor,Hostname,Ip,Status,Comments) values \
  (\"$vendor\",\"$hostname\",\"$ip\",\"$status\",\"$date $time\");\r"
  #send_error "SQL INSERT $ip\n"
  expect "sqlite"
  send "commit;\r"
  expect "sqlite"
}




# Don't check keys
spawn ssh -o StrictHostKeyChecking=no $username\@$ip -p $ssh_port

# Please don't change the following timeout value
set timeout 8




# Create a history log file
log_file -a logs/history.log


expect {
timeout {
 loggit $hostname $ip "${red} Timeout Exceeded ${normal}" "logs/failed.log"
 send_sql $vendor $hostname $ip "Timeout Exceeded" $date $time $sec
exit 1
}
eof {
 loggit $hostname $ip "${red} $expect_out(buffer) ${normal}" "logs/failed.log"
 send_sql $vendor $hostname $ip "$expect_out(buffer)" $date $time $sec
 exit 1
}
"*assword" {
send "$password\r"
expect "*assword" {
 loggit $hostname $ip "${red} The username or password is incorrect ${normal}" "logs/failed.log"
 send_sql $vendor $hostname $ip "The username or password is incorrect" $date $time $sec
 exit 1
}
}
}

log_file


# Log results are saved on the following directory
file mkdir logs/offlinecopies/$hostname-$ip
set log_directory "logs/offlinecopies/$hostname-$ip/$hostname-$ip--$date--$time.log"
log_file -a $log_directory

# if the script got enable prompt '>' what should it do
expect {
  "*>" {
    send "enable\r"
    expect "*assword"
    send "$enpasswd\r"
    expect "% Access denied" {
    send_error "\n"
    loggit $hostname $ip "${red} Enable password is incorrect ${normal}" "logs/failed.log"
    exit 1
    }
    }
    }

# just to print a new line
send "\r"
expect "*#"

# changing the default terminal lenght value from 24 to 0 so that show command
# doesn't display --More-- in the log files.
send "terminal length 0\r"
expect "*#"

# Iterate over the configuraton commands to execute them one by one.
set f [open "./vendor/cisco/commands.txt"]
set cmds [split [read $f] "\n"]
close $f

set timeout 5
# start sending the commands to the targeted device
foreach cmd $cmds {
  send "$cmd\r"
  # if the cmd starts with "sh" or "show" then assign the first word to f
  set f [join [lrange [split $cmd] 0 0 ]]
  # if the cmd starts with "do sh" or "do show" then assign the first and the second word to s
  set s [join [lrange [split $cmd] 0 1 ]]
  # if the user miss typed a show command, the next commands are allowed to be executed.
  if { $f == $sh || $f == $show || $s == $do_sh || $s == $do_show } {
    expect {
    "% Unknown command or computer name*" {
      log_file
      send_error "$hostname > $ip >> ${red} Unknown show command detected ${normal} >>> $cmd\n"
      log_file -a $log_directory
    }
    "% Ambiguous command*" {
      log_file
      send_error "$hostname > $ip >> ${red} Ambiguous show command detected ${normal} >>> $cmd\n"
      log_file -a $log_directory
    }
    "% Invalid input detected*" {
      log_file
      send_error "$hostname > $ip >> ${red} Invalid show command detected ${normal} >>> $cmd\n"
      log_file -a $log_directory
    }
    "% Incomplete command*" {
      log_file
      send_error "$hostname > $ip >> ${red} Incomplete show command detected ${normal} >>> $cmd\n"
      log_file -a $log_directory
    }
    }
    } else {
    # if the user miss typed a configuration commmand, the next commands will not be
    # executed and the program will exit.
    expect {
      -re "Unknown command|Invalid input|Ambiguous command|Incomplete command" {
        loggit $hostname $ip "${red} Unrecognized command has been detected ${normal} >>> $cmd" "logs/partial.log"

        send_sql $vendor $hostname $ip "check cmd $cmd" $date $time $sec

        exit 1
  }
}
}
}


send "\n"
expect "*#"

send_sql $vendor $hostname $ip "success" $date $time $sec


loggit $hostname $ip "${green} Successfully deployed the commands ${normal}" "logs/history.log"


exit 1
