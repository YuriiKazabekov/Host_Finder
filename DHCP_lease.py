import subprocess
import pexpect
import getpass
from init import *
from datetime import datetime


# переменная в которой храниться дата создания конфига
formatted_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

DHCP_user = 'Y.Kazabekov'
DHCP_password = getpass.getpass(prompt='DHCP_password:')


DHCP_ip = ['10.0.7.199']
Lease_list = ['10.0.1.0', '10.0.2.0', '10.0.3.0', '10.0.4.0','10.0.5.0', '10.0.6.0', '10.0.16.0', '10.0.20.0', '10.0.24.0', '10.10.30.0', '10.10.31.0' ]              



for ip in DHCP_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh -l {} {}'.format(DHCP_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices
        '''try:
            ssh.expect('[(yes/no?)>]')
            ssh.sendline('yes')
        except:
            pass'''

        ssh.expect('password:')
        ssh.sendline(DHCP_password)

        #ssh.expect('[>]')
        #ssh.sendline('powershell.exe')
        
        ssh.expect('[>]')
        ssh.sendline('powershell.exe')
        
       
        ssh.expect('[>]')
        
        for lease in Lease_list:
            ssh.sendline(r'Get-DhcpServerv4Lease -ScopeId {} | Select-Object -Property ClientId, IPAddress, HostName |  Export-Csv -Path C:\Users\Y.Kazabekov\{}.csv'.format(lease, lease))
        #ssh.sendline(r'Get-DhcpServerv4Lease -ScopeId 10.0.2.0 |  Export-Csv -Path C:\Users\Y.Kazabekov\10.0.2.0.csv')
        
        
        
        ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
        #bbb = ssh.before.decode('ascii')
        
        
        #f = open('myfile.txt', 'w')
        #f.write(bbb)  # python will convert \n to os.linesep
        #f.close()
        
        #print(bbb)
        #print(ssh.before.decode('ascii'))
        ssh.close()


for ip in Lease_list:
    subprocess.call(["rm", "-r", "/home/appliance/venv/lease/{}.csv".format(ip)])



for ip in DHCP_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh -l {} {}'.format(DHCP_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

        
        ssh.expect('password:')
        ssh.sendline(DHCP_password)

        
        
        ssh.expect('[>]')
        ssh.sendline(r'cd C:\Program Files (x86)\WinSCP')
        
        
        ssh.expect('[>]')
        ssh.sendline('winscp')
        
        ssh.expect('winscp>')
        ssh.sendline('open sftp://appliance:BronzePunish2018@10.0.14.71/')
        
        
        ssh.expect('winscp>')
        
        for lease in Lease_list:
            ssh.sendline(r'put "C:\Users\Y.Kazabekov\{}.csv " /home/appliance/venv/lease/'.format(lease))
        #ssh.sendline(r'put "C:\Users\Y.Kazabekov\10.0.1.0.csv" /home/appliance/venv/lease/')
        
        ssh.expect('winscp>')
        ssh.sendline('exit')
        ssh.close()