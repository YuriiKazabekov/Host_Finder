import pexpect
import getpass
from init import *
from datetime import datetime


# переменная в которой храниться дата создания конфига
formatted_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


#user = 'admin'
#password = getpass.getpass()

ACSW_user = 'admin'
ACSW_password = getpass.getpass(prompt='ACSW_password:')


ACSW_ip = ['10.0.1.250', '10.0.1.251', '10.0.1.252', '10.0.2.250', '10.0.2.251', '10.0.2.252',  '10.0.3.250', '10.0.3.251',  #'10.0.2.253',
             '10.0.3.252', '10.0.3.253' , '10.0.4.250', '10.0.4.251', '10.0.4.252', '10.0.5.250', '10.0.5.251', '10.0.5.252', '10.0.5.253',
             '10.0.6.250', '10.0.6.251', '10.0.6.253']
              


for ip in ACSW_ip:
    print('Connection to device {}'.format(ip))
    with pexpect.spawn('ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc {}@{}'.format(ACSW_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

        ssh.expect('[(yes/no?)>]')
        ssh.sendline('yes')

        ssh.expect('password:')
        ssh.sendline(ACSW_password)

        ssh.expect('[#>]')
        ssh.sendline('show fdb')
       
        ssh.expect('[CTRL+C ESC q Quit SPACE n Next Page ENTER Next Entry a All>]')
        ssh.sendline('a')
        
        ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
        bbb = ssh.before.decode('ascii')
        
        
        f = open('/mnt/c/Users/Y.Kazabekov/projects/Network_utilities/fdb/{}_fdb.txt'.format(ip), 'w')
        f.write(bbb)  # python will convert \n to os.linesep
        f.close()
        
        
        #print(bbb)
        ssh.close()


    with open('/mnt/c/Users/Y.Kazabekov/projects/Network_utilities/fdb/{}_fdb.txt'.format(ip)) as file:
        array = [row.strip() for row in file]
        new_array = []
      
    for i in array:
        if 'Forward' in i:
            new_array.append(i)
        else:
            pass
            
    final_array = []        
    for i in new_array:
        if 'T1' not in i :
            #i = ' '.join(i.split()) #Оставляет только один пробел
            final_array.append(i)
            f = open('/mnt/c/Users/Y.Kazabekov/projects/Network_utilities/parsed_fdb/{}.txt'.format(ip), 'w')
            for item in final_array:
                f.write("%s\n" % item)  
            f.close()
