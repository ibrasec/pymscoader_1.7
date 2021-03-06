

#!/usr/bin/expect -f

# This program is used to execute a group of cisco "show" commands stored on showcmds.txt file
# on a single host device... if the showcmds.txt file is empty then "show running" command will
# be sent to the targetted deviceS mentioned in the iplist.txt file
# Done by Ibrahim Abdulghni Khorwat
# To trigger this program, simlpy type the below on your linux shell
# ./expectrun.sh 192.168.1.1 username password enablepasword
# example:
# user@user$./runexpect 10.1.1.1 noshrun username password enablepassword
# user@user$./runexpect 10.1.1.1 shrun username password enablepassword

# Set variables
set device [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set enpasswd [lindex $argv 3]
set date [exec date +%F]
set sec [clock seconds]
set time [clock format $sec -format %H-%M-%S]

# Don't check keys
spawn ssh -o StrictHostKeyChecking=no $username\@$device

# Please don't change the following timeout value
set timeout 1


# Announce device & time
send_user "\n"
send_user ">      Working on $device @ [exec date]     <\n"


send_user "\n"

expect {
timeout { send_error "\nTimeout Exceeded - Check connectivity with Host $device\n";exit 1 }
eof { send_error "\nSSH Connection To $device Failed\n"; exit 1 }
"*assword" {
send "$password\r"
expect "*assword" {
  send_error "\n"
  send_error "\nError processing $device: The specified username or password is incorrect, please try again\n"
  exit 1
}
}
}

log_file


# if the script got enable prompt '>' what should it do
expect {
  "*>" {
    send "enable\r"
    expect "*assword"
    send "$enpasswd\r"
    expect "*assword" {
    send_error "\n"
    exit 1
    }
    }
    }


# just to print a new line
send "\r"
expect "#"
send "config router\r"
expect "*>config>router>"


for {set id 1} {$id < 254} {incr id 1} {
send "interface loopback$id\r"
expect "*>config>router>if\$"
send "ip address 1.2.1.$id/32\r"
send "exit"
sleep 0.05
}

send "exit\r"
expect "*>config>>config>"
send_user "\n"
