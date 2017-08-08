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
import netaddr.core
from netaddr import IPNetwork
from mini_logger import log

def isvalidip(ip):
    '''
    To check if the passed ip address is a valid ipv4 or ipv6 address
    example:
    >>>isvalidip('10.1.1.1')
    True
    >>>isvalidip('10.1.1.1.')
    False
    >>>isvalidip('2001:db8::1/120')
    True
    '''
    try:
        IP = IPNetwork(ip.strip())
        return True
    except netaddr.core.AddrFormatError:
        return False
    except ValueError:
        return False


def call_targets(excluded_list=[],default_vendorname='cisco'):
    '''
    This function is to make it very easy for the user to enter
    a whole subnet instead of writing each ip address individually
    in the  < ip_list.txt > file. it also gives the user the ability
    to specify the vendor and the hostname associated with that ip address.

    The Default vendor and hostnames are cisco, you can change this value to
    be another vendor by using -d option when you execute the program.
    ex:
    $python pymscoader -d huawei

    The following is an examples of what could be the format of the ip_list.txt
    file in order for the program to work as required:
    10.1.1.0/30
    router-01,10.1.2.1
    huawei,router-02,172.16.1.1
    router-03,huawei,172.16.12.10
    switch-01,2001:db8::1/128
    '''
    # setting default variables
    subnets = []
    vendors = os.listdir('vendor')
    vendorname = hostname = default_vendorname
    got_vendor = False
    excluded_ip_addresses = 0
    # UPDATE: THERE WAS NO PORT
    ssh_port = '22'
    # reading the ip_list.txt file
    with open("ip_list.txt") as iplist_h:
        subnet_list = iplist_h.readlines()
        # making sure that the ip_list.txt file has been populated with IP addresses
        if len(subnet_list) == 0 or subnet_list == ['\n'] :
           log("[!] The (ip_list.txt) file should include at least one ip address.")
           log("The program will exit. ")
           exit()
    # start passing through ip_list.txt lines
    for line in subnet_list:
        # making each line as a list of [vendor,Hostname,ip_Address]
        items = line.split(',')
        if len(items) <=3:
            # collecting valid ipv4/ipv6 addresses and subnets
            # UPDATE: THERE WAS NO ip and no (if "#" in items[-1])
            ip = items[-1].split("#")[0].strip()
            if "#" in items[-1]:
                ssh_port =  items[-1].split("#")[1].strip()
            # UPDATE: it was
            #if isvalidip(items[-1].strip()):
            #    IPs = list( IPNetwork( items[-1].strip() ) )
            if isvalidip(ip):
                IPs = list( IPNetwork( ip ) )
            else:
                log("Error: An invalid IPv4/IPv6 address has been detected => ",items[-1].strip())
                log("       This address will be ignored.\n")
                continue
            # exctracting vendor names and hostnames from each line
            for item in items[:-1]:
                for v in vendors:
                    if v == item.strip().lower():
                        vendorname = v
                        got_vendor = True
                        vendor_index = items.index(item)
                        continue
            # ignoring lines that has no vendor name matched the existed vendor list (vendors)
            # example: ['newvendor','router-01','2001:db8::1/128']
            if not got_vendor and len(items[:-1]) == 2:
                log('Error: Currently neither \"',items[0],'\" nor \"',items[1],'\" are recognized as supported vendor names')
                log("       The only supported vendor names are:")
                log("      ",vendors)
                log("       This line will be ignored =>",items,'\n')
                continue
            # extracting the hostname for items simliar to ['router-01','192.168.1.0/23']
            elif len(items[:-1])==1:
                hostname = item
            # for items simliar to ['192.168.1.0'] the default hostname will be chosen
            elif len(items[:-1])==0:
                pass
            # extracting the hostname for items similar to ['router-01','cisco','192.168.2.0/28']
            else:
                hostname = items[1-vendor_index]
            # getting individual ip addresses from a complete subnet
            # ex: 10.1.1.0 to 10.1.1.3 for subnet 10.1.1.0/30
            for IP in IPs:
                # if the user choose to execlude some ip addresses, they will be will be ignored
                if str(IP) not in excluded_list:
                    # UPDATE: It was
                    # subnets.append((vendorname , hostname , str(IP)))
                    subnets.append((vendorname , hostname , str(IP) + "#" + ssh_port ))
                else:
                    excluded_ip_addresses += 1
        # Warning the user not to exceed 3 items per line
        else:
            log("Error: An invalid line has been detected:", line.strip() )
            log("Please make sure that each line in the ip_list.txt file doesn't exceed 3 items at maximum")
            log("example:")
            log("cisco , router-01 , 192.168.1.1\n")
            log("cisco , 192.168.2.1/24\n")
            log("2001:db8::1/128\n")
            # To print and log
    if len(excluded_list) > 0:
        log('[!] There are',excluded_ip_addresses,'detected ip addresses to be excluded')
    #print subnets
    return subnets

if __name__ == '__main__':
    call_targets()
