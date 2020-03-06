import pexpect
import getpass
import paramiko
import time
from datetime import datetime


# переменная в которой храниться дата создания конфига
formatted_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# переменная с IP сервера TFTP
tftp_server = '10.0.4.79'

#user = 'admin'
#password = getpass.getpass()

ACSW_user = 'admin'
ACSW_password = '!DGS3120#'
#ACSW_password = getpass.getpass(prompt='ACSW_password:')

FG_user = 'net-admin'
#FG_password = getpass.getpass(prompt='FG_password:')
FG_password = 'BronzePunish2018'

ACSW_ip = ['10.0.1.250', '10.0.1.251', '10.0.1.252', '10.0.2.250', '10.0.2.251', '10.0.2.252',  '10.0.3.250', '10.0.3.251',  '10.0.2.253']#,
              #'10.0.3.252', '10.0.3.253' , '10.0.4.250', '10.0.4.251', '10.0.4.252', '10.0.5.250', '10.0.5.251', '10.0.5.252', '10.0.5.253',
              #'10.0.6.250', '10.0.6.251', '10.0.6.253']
              
FG_ip = ['10.0.10.5']#, '10.10.20.254', '10.10.30.254', '10.10.20.254']              
              
def backup(show_result):
    #show_result = []
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
            l = ssh.before.decode('ascii')
            show_result.append(l)
            ssh.close()

    for ip in FG_ip:
        print('Connection to device {}'.format(ip))
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=ip,
            port='2202',
            username=FG_user,
            password=FG_password,
            look_for_keys=False,
            allow_agent=False)

        with client.invoke_shell() as ssh:
        
            ssh.send('execute backup config tftp /Fortigate/{}_{}.conf {}\n'.format(ip, formatted_date, tftp_server))
            time.sleep(1)
            l = ssh.recv(5000).decode('ascii')
            show_result.append(l)

        

        client.close()
    return(show_result)
    
   