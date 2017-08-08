failed_ips = []

def pass_fail(target_list):
    ip_list = [ ip[2] for ip in target_list ]
    with open('log/failed.txt','r') as fh:
        l=fh.readlines()
        for i in l[2:]:
            failed_ips.append(i.split('>')[1].strip())

    for ip in failed_ips:
        ip_list.remove(ip)

    return failed_ips,ip_list

def send_email(target_list,email_list):
    message_body = ...
