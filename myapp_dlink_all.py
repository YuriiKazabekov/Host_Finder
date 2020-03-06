import pexpect
import getpass
import paramiko
import subprocess
import mysql.connector
import csv
from init import *
from datetime import datetime
import time










conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='###',
                                      autocommit=True)

cursor = conn.cursor()

#now = datetime.now()
################ D-LINK DGS 3120, 3420##################################
ACSW_user = '###'
#ACSW_password = getpass.getpass(prompt='ACSW_password:')
ACSW_password = '###'

SSW_1_user = '###'
#SSW_1_password = getpass.getpass(prompt='SSW_1_password:')
SSW_1_password = '###'

SSW_2_user = '###'
#SSW_2_password = getpass.getpass(prompt='SSW_2_password:')
SSW_2_password = ACSW_password = '###'

SSW_3_user = '###'
#SSW_3_password = getpass.getpass(prompt='SSW_3_password:')
SSW_3_password = ACSW_password = '###'

ACSW_ip = ['10.0.1.250', '10.0.1.251', '10.0.1.252', '10.0.2.250', '10.0.2.251', '10.0.2.252', '10.0.2.253', '10.0.3.250', '10.0.3.251',  
             '10.0.3.252', '10.0.3.253' , '10.0.4.250', '10.0.4.251', '10.0.4.252', '10.0.5.250', '10.0.5.251', '10.0.5.252', '10.0.5.253',
             '10.0.6.250', '10.0.6.251', '10.0.6.253', '10.10.30.251']
SSW_1_ip = ['10.0.7.250']
SSW_2_ip = ['192.168.3.254']
SSW_3_ip = ['10.0.15.250']

#D_LINK_ip = ACSW_ip + SSW_1_ip + SSW_2_ip + SSW_3_ip
#print (D_LINK_ip)
################ D-LINK DGS 1210########################################
ACSW_1210_user = '###'
#ACSW_1210_password = getpass.getpass(prompt='ACSW_1210_password:')
ACSW_1210_password = '###'

ACSW_1210_ip = ['10.0.5.241', '10.10.30.250']

################ CISCO SG-500, SG-350 ###################################
CISCO_switches_user = '###'
#CISCO_switches_password = getpass.getpass(prompt='CISCO_switches_password:')
CISCO_switches_password = '###'

CISCO_switches_ip = ['10.10.20.250', '10.10.20.251', '10.0.15.249', '10.0.7.254'] 

################ HP, Aruba 2350 ##########################################
Aruba_switches_user = '###'
#Aruba_switches_password = getpass.getpass(prompt='Aruba_switches_password:')
Aruba_switches_password = '###'

Aruba_switches_ip = ['10.10.30.252']
################ FG fdb ##########################################

FG_fdb_ip = ['10.10.40.254']
#################### all_switches_ip ####################################
all_switches_ip = ACSW_ip + SSW_1_ip + SSW_2_ip + SSW_3_ip + ACSW_1210_ip + CISCO_switches_ip + Aruba_switches_ip + FG_fdb_ip
print(all_switches_ip)
################ Windows DHCP server######################################
#require installed ssh and winscp 
DHCP_user = '###'
#DHCP_password = getpass.getpass(prompt='DHCP_password:')
DHCP_password = '###'

DHCP_ip = ['10.0.7.199', '10.0.15.252']
#list of leases 
Lease_list_1 = ['10.0.1.0', '10.0.2.0', '10.0.3.0', '10.0.4.0','10.0.5.0', '10.0.6.0', '10.0.16.0', '10.0.20.0', '10.0.24.0', '10.10.30.0', '10.10.31.0' ] 
Lease_list_2 = ['10.0.12.0']
################ Fortigate DHCP server######################################
FG_user = '###'
#FG_password = getpass.getpass(prompt='FG_password:')
FG_password = '###'

FG_ip = ['10.10.20.254', '10.10.40.254']


############################################################################################################################################################################################
###################################################################             FDB             ############################################################################################
############################################################################################################################################################################################
#Ця функція підключається до комутаторів, зберігає таблицю mac_address парсить та записує до файлів {switch_ip}_fdb.txt
# переменная в которой храниться дата создания конфига

              
def ACSW_fdb():

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
            
            ssh.expect('#')
            #ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            bbb = ssh.before.decode('ascii')
            
            
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
            
            
            #print(bbb)
            ssh.close()


        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
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
                f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
                for item in final_array:
                    f.write("%s\n" % item)  
                f.close()
        print('OK')
#################################################################################################################
def SSW_1_fdb():

    for ip in SSW_1_ip:
        print('Connection to device {}'.format(ip))
        with pexpect.spawn('ssh -o KexAlgorithms=diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-dss {}@{}'.format(SSW_1_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

            ssh.expect('[(yes/no?)>]')
            ssh.sendline('yes')

            ssh.expect('password:')
            ssh.sendline(SSW_1_password)

            ssh.expect('[#>]')
            ssh.sendline('show fdb')
           
            ssh.expect('[CTRL+C ESC q Quit SPACE n Next Page ENTER Next Entry a All>]')
            ssh.sendline('a')
            
            ssh.expect('#')
            #ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            bbb = ssh.before.decode('ascii')
            
            
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
            
            
            #print(bbb)
            ssh.close()


        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
            new_array = []
          
        for i in array:
            if 'Forward' in i:
                new_array.append(i)
            else:
                pass
                
        final_array = []        
        for i in new_array:
            #if '1:49' not in i:
            if 'T22' not in i:
                #i = ' '.join(i.split()) #Оставляет только один пробел
                final_array.append(i)
                f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
                for item in final_array:
                    f.write("%s\n" % item)  
                f.close()
        print('OK')
###############################################################################################################################
def SSW_2_fdb():

    for ip in SSW_2_ip:
        print('Connection to device {}'.format(ip))
        with pexpect.spawn('ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc {}@{}'.format(SSW_2_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

            ssh.expect('[(yes/no?)>]')
            ssh.sendline('yes')

            ssh.expect('password:')
            ssh.sendline(SSW_2_password)

            ssh.expect('[#>]')
            ssh.sendline('show fdb')
           
            ssh.expect('[CTRL+C ESC q Quit SPACE n Next Page ENTER Next Entry a All>]')
            ssh.sendline('a')
            
            ssh.expect('#')
            #ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            bbb = ssh.before.decode('ascii')
            
            
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
            
            
            #print(bbb)
            ssh.close()


        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
            new_array = []
          
        for i in array:
            if 'Forward' in i:
                new_array.append(i)
            else:
                pass
                
        final_array = []        
        for i in new_array:
            #if '1:23' not in i :
            if 'T23' not in i :
                #i = ' '.join(i.split()) #Оставляет только один пробел
                final_array.append(i)
                f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
                for item in final_array:
                    f.write("%s\n" % item)  
                f.close() 
        print('OK')
#################################################################################################
def SSW_3_fdb():

    for ip in SSW_3_ip:
        print('Connection to device {}'.format(ip))
        with pexpect.spawn('ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc {}@{}'.format(SSW_3_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices

            ssh.expect('[(yes/no?)>]')
            ssh.sendline('yes')

            ssh.expect('password:')
            ssh.sendline(SSW_3_password)

            ssh.expect('[#>]')
            ssh.sendline('show fdb')
           
            ssh.expect('[CTRL+C ESC q Quit SPACE n Next Page ENTER Next Entry a All>]')
            ssh.sendline('a')
            
            ssh.expect('#')
            #ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            bbb = ssh.before.decode('ascii')
            
            
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
            
            
            #print(bbb)
            ssh.close()


        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
            new_array = []
          
        for i in array:
            if 'Forward' in i:
                new_array.append(i)
            else:
                pass
                
        final_array = []        
        for i in new_array:
            if 'T24' not in i :
                #i = ' '.join(i.split()) #Оставляет только один пробел
                final_array.append(i)
                f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
                for item in final_array:
                    f.write("%s\n" % item)  
                f.close()                            
        print('OK')
######################################################################################################

def ACSW_1210_fdb():

    for ip in ACSW_1210_ip:
        print('Connection to device {}'.format(ip))
        with pexpect.spawn('telnet {}'.format( ip)) as telnet:       

            telnet.expect('[login:>]')
            telnet.sendline(ACSW_1210_user)

            telnet.expect('Password:')
            telnet.sendline(ACSW_1210_password)

            telnet.expect('[>]')
            telnet.sendline('debug info')
            for i in range(25):
                time.sleep(1)
                telnet.sendline(' ')
            
            
            #telnet.expect([pexpect.TIMEOUT, pexpect.EOF])
            telnet.expect('>')
            bbb = telnet.before.decode('ascii')
            telnet.close()
            
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
                        
            telnet.close()

        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
            new_array = []
                  
        for i in array:
            if 'Learnt' in i:
                i1 = i.replace("[K", "")
                i2 = i1.replace(":", "-")
                i3 = i2.replace("  Learnt  ", " ")
                i = i3.replace("     ", "  VLAN_NAME  ")
                i = i + '  Dynamic  ' + '  Forward  '
                new_array.append(i)
            else:
                pass
                
        final_array = []        
        for i in new_array:
            if (ip == '10.0.5.241' and 'Gi0/48' not in i) or (ip == '10.10.30.250' and 'Gi0/24' not in i) :
           # This if delete mac assigned from wan port
                final_array.append(i)
                f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
                for item in final_array:
                    f.write("%s\n" % item)  
                f.close()
        print('OK')        
#######################################################################################################################
def CISCO_fdb():
    for ip in CISCO_switches_ip:
        if ip == '10.0.7.254':
            print('Connection to device {}'.format(ip))
            with pexpect.spawn('ssh {}@{}'.format(CISCO_switches_user, ip)) as ssh:        

                ssh.expect('password:')
                ssh.sendline(CISCO_switches_password)

                ssh.expect('[#>]')
                #ssh.sendline('show mac address-table interface GigabitEthernet2/1/30')  
                ssh.sendline('show mac address-table vlan 250') 
                ssh.expect('<return>')
                aaa = ssh.before.decode('ascii')
                ssh.sendline('a')   
                #ssh.expect('CSW#')
                #ssh.sendline('show mac address-table interface GigabitEthernet2/1/32')
                #ssh.expect('<return>')
                #ssh.sendline('a')
                ssh.expect('CSW#')
                bbb = ssh.before.decode('ascii')
                 
                f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
                f.write(aaa)
                f.write(bbb)  # python will convert \n to os.linesep
                f.close()
                ssh.close()
        else:
            print('Connection to device {}'.format(ip))
            with pexpect.spawn('ssh {}@{}'.format(CISCO_switches_user, ip)) as ssh:   
            
                ssh.expect('password:')
                ssh.sendline(CISCO_switches_password)
                ssh.expect('[#>]')
                ssh.sendline('show mac address-table')    
                ssh.expect('<return>')
                aaa = ssh.before.decode('ascii')
                ssh.sendline('a')
                ssh.expect('#')
                    
                #ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
                #ssh.expect([pexpect.EOF, timeout=None])
                bbb = ssh.before.decode('ascii')
                    
                
                
                f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
                f.write(aaa)
                f.write(bbb)  # python will convert \n to os.linesep
                f.close()
                    
                    
                #print(bbb)
                ssh.close()        
                
        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
        new_array = []
              
        for i in array:
            if 'dynamic' in i:
                new_array.append(i)
            else:
                pass
                    
        final_array = []        
        for i in new_array:
            if 'te1/0/12' not in i and 'Po1' not in i:
                i1 = i.replace(":", "-")
                i2 = i1.replace("       ", "  VLAN_NAME  ")
                i = i2.replace("dynamic", "Dynamic Forward")
                final_array.append(i)
                #print(i)
            else:
                pass
        f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
        for item in final_array:
            f.write("%s\n" % item)  
        f.close()





        print('OK')        
# cisco switches
def Aruba_fdb():

    for ip in Aruba_switches_ip:
        print('Connection to device {}'.format(ip))
        with pexpect.spawn('ssh {}@{}'.format(Aruba_switches_user, ip)) as ssh:       

            ssh.expect('password:')
            ssh.sendline(Aruba_switches_password)

            ssh.expect('Press any key to continue')
            ssh.sendline(' ')
            
            ssh.expect('#')
            ssh.sendline('show mac-address')
            
            for i in range(10):
                time.sleep(1)
                ssh.sendline(' ')           
 
            #ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            #ssh.expect('HP-2530-48G#')
            ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            bbb = ssh.before.decode('utf8')
            ssh.close()
            
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(bbb)  # python will convert \n to os.linesep
            f.close()
                        
            ssh.close()

        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
            new_array = []
                  
        for i in array:
            #if 'Trk1' not in i and '    2' in i:
            #    i1 = i.replace("[24;1H", "")
            #    i2 = i1.replace("MORE --, next page: Space, next line: Enter, quit: Control-C", "")
            #    i3 = i2.replace("[2K-- [2K[1;24r  ", "")
            #    i4 = i3[0:2] + '-' + i3[2:4] + '-' + i3[4:6] + i[6:9] + '-' + i[9:11] + '-' + i[11:]
            #    i5 = i4[26:] + "  VLAN_NAME  " + i4[0:26] + '  Dynamic  ' + '  Forward  '
            #    new_array.append(i5)
                
            if 'Trk1' not in i and '    2' in i:
                i1 = i.replace("[24;1H", "")
                i1 = i1.replace("MORE --, ", "")
                i1 = i1.replace("next page: ", "")
                i1 = i1.replace("Space", "")
                i1 = i1.replace(",", "")
                i1 = i1.replace("quit:", "")
                i1 = i1.replace("Control-C", "")
                i1 = i1.replace("[24;1H", "")
                i1 = i1.replace("[24;1H", "")
                i2 = i1.replace("[1;24r", "")
                i3 = i2.replace("[2K-- [2K[1;24r  ", "")
                i4 = i3[0:2] + '-' + i3[2:4] + '-' + i3[4:6] + i[6:9] + '-' + i3[9:11] + '-' + i3[11:]
                i5 = i4[26:] + "  VLAN_NAME  " + i4[0:26] + '  Dynamic  ' + '  Forward  '
                new_array.append(i5)
            else:
                pass
                
        final_array = []        
        for i in new_array:
           # if (ip == '10.0.5.241' and 'Gi0/48' not in i) or (ip == '10.10.30.250' and 'Gi0/24' not in i) :
           # This if delete mac assigned from wan port
            final_array.append(i)
            f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
            for item in final_array:
                f.write("%s\n" % item)  
            f.close()
        print('OK') 
        
        
def fg_fdb():
    for ip in FG_fdb_ip:
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
        
            ssh.send('diag ip arp list\n')
            time.sleep(0.5)
            result = ssh.recv(5000).decode('ascii')
            #print(result)
            
        
            f = open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip), 'w')
            f.write(result)  # python will convert \n to os.linesep
            f.close()
        client.close()
        
        with open('/home/appliance/venv/fdb/{}_fdb.txt'.format(ip)) as file:
            array = [row.strip() for row in file]
            new_array = []
                  
        for i in array:
            if 'internal' in i:
            
                keyword = 'internal'
                before_keyword, keyword, after_keyword = i.partition(keyword)
                i = after_keyword
                keyword = 'state'
                before_keyword, keyword, after_keyword = i.partition(keyword)       
                i = before_keyword
                i = i[-18:]
                i1 = '1  VLAN_NAME         ' + i.replace(":", "-") + 'Int    Dynamic     Forward'
                new_array.append(i1)
                

            else:
                pass
                
        final_array = []        
        for i in new_array:
            final_array.append(i)
            f = open('/home/appliance/venv/parsed_fdb/{}_fdb.txt'.format(ip), 'w')
            for item in final_array:
                f.write("%s\n" % item)  
            f.close()
        print('OK') 
############################################################################################################################################################################################
###################################################################             LEASE             ##########################################################################################
############################################################################################################################################################################################
#Ця функція підключається до DHCP серверу та зберігає dhcp lease до файлів {lease_ip}.csv

def lease():

    for ip in DHCP_ip:
        if ip == '10.0.7.199':
            Lease_list = Lease_list_1
        else:
            Lease_list = Lease_list_2
        print('Connection to device {}'.format(ip))
        with pexpect.spawn('ssh -l {} {}'.format(DHCP_user, ip)) as ssh:        #-oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-cbc ad it for connecting to old devices
            '''try:
                ssh.expect('[(yes/no?)>]')
                ssh.sendline('yes')
            except:
                pass'''

            ssh.expect('password:')
            ssh.sendline(DHCP_password)
            
            ssh.expect('[>]')
            ssh.sendline('powershell.exe')
            
            ssh.expect('[>]')
            
            for lease in Lease_list:
                ssh.sendline(r'Get-DhcpServerv4Lease -ScopeId {} | Select-Object -Property ClientId, IPAddress, HostName |  Export-Csv -Path C:\Users\Y.Kazabekov\{}.csv'.format(lease, lease))
            
            ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
            ssh.close()

    for ip in Lease_list_1:
        subprocess.call(["rm", "-r", "/home/appliance/venv/lease/{}.csv".format(ip)])
    for ip in Lease_list_2:
        subprocess.call(["rm", "-r", "/home/appliance/venv/lease/{}.csv".format(ip)])
        
    for ip in DHCP_ip:
        if ip == '10.0.7.199':
            Lease_list = Lease_list_1
        else:
            Lease_list = Lease_list_2
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
            
            for ip in Lease_list:
                ssh.sendline(r'put "C:\Users\Y.Kazabekov\{}.csv " /home/appliance/venv/lease/'.format(ip))
            
            ssh.expect('winscp>')
            ssh.sendline('exit')
            ssh.close()
        
        print('OK')
        
        
        
        
        
        

############################################################################################################################################################################################
###################################################################             MYSQL UPDATER             ##################################################################################
############################################################################################################################################################################################
def fg_lease():
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
        
            ssh.send('execute dhcp lease-list\n')
            time.sleep(0.5)
            result = ssh.recv(5000).decode('ascii')
            #print(result)
        
        
            f = open('/home/appliance/venv/lease/{}.csv'.format(ip), 'w')
            f.write(result)  # python will convert \n to os.linesep
            f.close()
        client.close()
        
        array = []
        with open('/home/appliance/venv/lease/{}.csv'.format(ip)) as file:
            array = [row.strip() for row in file]
            
        new_array = []  
        for i in array:
            if '10.10' in i:
                i1 = i.replace(":", "-")
                i = '\t'.join(i1.split())
                new_array.append(i)
            else:
                pass
        #print(new_array) 
        final_array = []
        for i in new_array:
            listed_i = i.split('\t')
            #print(listed_i)
            final_array.append(listed_i)
        #f = open('/home/appliance/venv/lease/{}.csv'.format(ip), 'w')
        #for item in new_array:
        #    f.write("%s\n" % item)  
        #f.close()


        for i in final_array:
            #print(i)
            try:  
                text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[1],i[0], i[2])
                cursor.execute(text_sql)
            except:
                text_sql = 'DELETE FROM lease WHERE IP = "{}"'.format(i[0])
                cursor.execute(text_sql) 
                text_sql = 'DELETE FROM lease WHERE hostname = "{}"'.format(i[2])
                cursor.execute(text_sql)
                text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[1],i[0], i[2])
                cursor.execute(text_sql)
        print('OK')






################################################################################################################################
def dbupdater():
    result_array = []
    #for file in ACSW_ip:
    #for file in D_LINK_ip:
    for file in all_switches_ip:
        print(file)
        switch_ip_address = file
        with open('/home/appliance/venv/parsed_fdb/'+ str(file) + '_fdb.txt') as file:
            array = [row.strip() for row in file]
            new_array = []
          
        for i in array:
            if ('Forward' in i and 'CPU' not in i) or 'dynamic' in i:
            #if 'CPU' not in i:
                new_array.append(i)
            else:
                pass
                
        final_array = []
        
        for i in new_array:
            if 'T1' not in i :
                final_array.append(i)         
                
                for item in final_array:
                    a = item.split()
                    mystring = str(switch_ip_address)
                    keyword = '_fdb.txt'
                    before_keyword, keyword, after_keyword = mystring.partition(keyword)
                    mystring = before_keyword
                    a.append(mystring)
                    result_array.append(a)
    ################# place for cisco mac table parser ##############
    #for row in result_array:
    #    print(row)      
    for i in result_array:
        try:
            text_sql = 'INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number, time_of_adding ) VALUES("{}",{},"{}","{}","{}")'.format(i[2],i[0], i[6], i[3], now.strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(text_sql)
            
        except:   
            text_sql = 'DELETE FROM fdb WHERE mac_address = "{}"'.format(i[2])
            cursor.execute(text_sql) 
            text_sql = 'INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number, time_of_adding ) VALUES("{}",{},"{}","{}","{}")'.format(i[2],i[0], i[6], i[3], now.strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(text_sql)
        
                
    ####################################################################################################################  LEASE
    """text_sql = 'SELECT mac_address FROM lease'
    cursor.execute(text_sql)
    result = cursor.fetchall()"""

    result_lease_array = []
    Lease_list = Lease_list_1+ Lease_list_2
    for file in Lease_list:
        print(file)
        with open('/home/appliance/venv/lease/'+file+'.csv', 'rU') as f:  #opens PW file
            reader = csv.reader(f)
            data = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists

            for row in data:
                if row[0] == '#TYPE Selected.Microsoft.Management.Infrastructure.CimInstance' or row[0] == 'ClientId':
                    pass
                else:
                    result_lease_array.append(row)                  
                 
    for i in result_lease_array:
        try:  
            #print(i)
            text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[0],i[1], i[2])
            cursor.execute(text_sql)
        except:
            text_sql = 'DELETE FROM lease WHERE IP = "{}"'.format(i[1])
            cursor.execute(text_sql) 
            #text_sql = 'DELETE FROM lease WHERE hostname = "{}"'.format(i[2])
            #cursor.execute(text_sql)
            text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[0],i[1], i[2])
            cursor.execute(text_sql)  

    ############## lease+voip update
    text_sql = 'DELETE FROM select_result'
    cursor.execute(text_sql)
    text_sql = 'INSERT INTO select_result SELECT lease.mac_address, lease.IP, lease.hostname, voip_users.hostname AS user_account, voip_users.phone_number AS phone_number, voip_users.useragent AS useragent FROM lease LEFT JOIN voip_users ON lease.IP = voip_users.IP ORDER BY lease.mac_address'
    cursor.execute(text_sql)
################################################################################################################################
##################################################VOIP##########################################################################
################################################################################################################################
#myapp.voip table updater for 

def voip():
    #text_sql = 'REPLACE INTO voip (mac_address , IP, vlan_ID, switch_IP, port_number) SELECT  fdb.mac_address, lease.IP, fdb.vlan_ID, fdb.switch_IP, fdb.port_number FROM fdb , lease  WHERE lease.mac_address = fdb.mac_address  AND  fdb.mac_address LIKE "00-0b-82%"'
    text_sql = 'REPLACE INTO voip (mac_address , IP, vlan_ID, switch_IP, port_number) SELECT fdb.mac_address, lease.IP, fdb.vlan_ID, fdb.switch_IP, fdb.port_number FROM fdb , lease, voip_users WHERE lease.mac_address = fdb.mac_address AND lease.IP = voip_users.IP'
    cursor.execute(text_sql)
    text_sql = 'SELECT  * FROM voip'
    cursor.execute(text_sql)
    result = cursor.fetchall()
################################################################################################################################
################################################################################################################################
################################################################################################################################ 






#################################################################################################################################
#################################################################################################################################           
while 1 != 2:
    try:
        ACSW_fdb()
    except:
        pass
    try:
        SSW_1_fdb()
    except:
        pass    
    try:
        SSW_2_fdb()
    except:
        pass 
    try:
        SSW_3_fdb()
    except:
        pass
    try:
        ACSW_1210_fdb()
    except:
        pass
    try:
        CISCO_fdb()
    except:
        pass 
    try:
        Aruba_fdb()
    except:
        pass 
    try:
        fg_fdb()
    except:
        pass      
    try:
        lease()
    except:
        pass
    now = datetime.now()
    try:
        fg_lease() 
    except:
        pass    
    try:
        dbupdater() 
    except:
        pass
    try:
        voip() 
    except:
        pass
    
    #text_sql = 'SELECT  fdb.mac_address, fdb.switch_IP, fdb.vlan_ID, lease.IP, lease.hostname, fdb.time_of_adding FROM fdb , lease  WHERE lease.mac_address = fdb.mac_address ORDER BY fdb.vlan_ID'
    #cursor.execute(text_sql)
    #result = cursor.fetchall()

    #for x in result:
    #    print(x)    
    #print(now)          
