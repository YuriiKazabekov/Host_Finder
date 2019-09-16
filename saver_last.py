import pexpect
import getpass
from init import *
from datetime import datetime


# переменная в которой храниться дата создания конфига
formatted_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# переменная с IP сервера TFTP, переместил в файл init.py
#tftp_server = '10.0.4.79'

#user = 'admin'
#password = getpass.getpass()

ACSW_user = 'admin'
ACSW_password = getpass.getpass(prompt='ACSW_password:')

FG_user = 'admin'
FG_password = getpass.getpass(prompt='FG_password:')

ACSW_ip = ['10.0.1.250', '10.0.1.251', '10.0.1.252', '10.0.2.250', '10.0.2.251', '10.0.2.252',  '10.0.3.250', '10.0.3.251',  #'10.0.2.253',
              '10.0.3.252', '10.0.3.253' , '10.0.4.250', '10.0.4.251', '10.0.4.252', '10.0.5.250', '10.0.5.251', '10.0.5.252', '10.0.6.250',
              '10.0.6.251', '10.0.6.253']
              
FG_ip = ['10.0.10.5']#, '10.10.20.254', '10.10.30.254', '10.10.20.254']              
              


for ip in ACSW_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc {}@{}'.format(ACSW_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

        ssh.expect('[(yes/no?)>]')
        ssh.sendline('yes')

        ssh.expect('password:')
        ssh.sendline(ACSW_password)

        ssh.expect('[#>]')
        ssh.sendline('save')
       
        ssh.expect('[#>]')
        ssh.sendline('upload cfg_toTFTP {} dest_file /ACSW/{}_{}.cfg'.format(tftp_server, ip, formatted_date))
        
        ssh.expect('#')
        print(ssh.before.decode('ascii'))
        ssh.close()



for ip in FG_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh {}@{}'.format(FG_user, ip)) as ssh:       

        ssh.expect('[(yes/no?)>]')
        ssh.sendline('yes')

        ssh.expect('password:')
        ssh.sendline(FG_password)
       
        ssh.expect('[#>]')
        ssh.sendline('execute backup config tftp /Fortigate/{}_{}.conf {}'.format(ip, formatted_date, tftp_server))
        
        ssh.expect('[OK>]')
        print(ssh.before.decode('ascii'))
        ssh.close()
