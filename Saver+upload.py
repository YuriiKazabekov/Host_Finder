import pexpect
import getpass
from datetime import datetime
#import sys

# создание переменной в которой храниться дата создания конфига
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d')
formatted_date


user = 'admin'
password = getpass.getpass()

devices_ip = ['10.0.1.250', '10.0.1.251', '10.0.1.252', '10.0.2.250', '10.0.2.251', '10.0.2.252',  '10.0.3.250', '10.0.3.251',  #'10.0.2.253',
              '10.0.3.252', '10.0.3.253' , '10.0.4.250', '10.0.4.251', '10.0.4.252', '10.0.5.250', '10.0.5.251', '10.0.5.252', '10.0.6.250',
              '10.0.6.251', '10.0.6.253']

for ip in devices_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc {}@{}'.format(user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

        ssh.expect('[(yes/no?)>]')
        ssh.sendline('yes')

        ssh.expect('password:')
        ssh.sendline(password)

        ssh.expect('[#>]')
        ssh.sendline('save')
       
        ssh.expect('[#>]')
        ssh.sendline('upload cfg_toTFTP 10.0.4.127 dest_file {}_{}.cfg'.format(ip, formatted_date))
        
        ssh.expect('#')
        print(ssh.before.decode('ascii'))
        ssh.close()