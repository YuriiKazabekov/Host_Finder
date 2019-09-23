import pexpect
import getpass
from init import *
from datetime import datetime


# переменная в которой храниться дата создания конфига
formatted_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

DHCP_user = 'Y.Kazabekov'
DHCP_password = getpass.getpass(prompt='DHCP_password:')


DHCP_ip = ['10.0.7.199']
Lease_ip = ['10.0.1.0', '10.0.2.0', '10.0.3.0', '10.0.4.0', '10.0.5.0', '10.0.6.0', '10.0.16.0', '10.0.20.0', '10.0.24.0']            


for ip in DHCP_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh -l {} {}'.format(DHCP_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

        #ssh.expect('[(yes/no?)>]')
        #ssh.sendline('yes')

        ssh.expect('password:')
        ssh.sendline(DHCP_password)

        #ssh.expect('[>]')
        #ssh.sendline('powershell.exe')
        
        ssh.expect('[>]')
        ssh.sendline('powershell.exe')
       

        ssh.expect('[>]')
        for ip in Lease_ip:
            ssh.sendline('Get-DhcpServerv4Lease -ScopeId {}'.format(ip))
        
            ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            bbb = ssh.before.decode('ascii')
        
        
            f = open('/mnt/c/Users/Y.Kazabekov/projects/Network_utilities/Lease/{}_Lease.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
        
            print(bbb)
        #print(ssh.before.decode('ascii'))
        ssh.close()