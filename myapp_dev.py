import pexpect
import getpass
import subprocess
import mysql.connector
import csv
from init import *
from datetime import datetime


conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)

cursor = conn.cursor()

now = datetime.now()

ACSW_user = 'admin'
ACSW_password = getpass.getpass(prompt='ACSW_password:')

DHCP_user = 'Y.Kazabekov'
DHCP_password = getpass.getpass(prompt='DHCP_password:')

ACSW_ip = ['10.0.1.250', '10.0.1.251', '10.0.1.252', '10.0.2.250', '10.0.2.251', '10.0.2.252',  '10.0.3.250', '10.0.3.251',  #'10.0.2.253',
             '10.0.3.252', '10.0.3.253' , '10.0.4.250', '10.0.4.251', '10.0.4.252', '10.0.5.250', '10.0.5.251', '10.0.5.252', '10.0.5.253',
             '10.0.6.250', '10.0.6.251', '10.0.6.253']



DHCP_ip = ['10.0.7.199']
Lease_list = ['10.0.1.0', '10.0.2.0', '10.0.3.0', '10.0.4.0','10.0.5.0', '10.0.6.0', '10.0.16.0', '10.0.20.0', '10.0.24.0', '10.10.30.0', '10.10.31.0' ]         








############################################################################################################################################################################################
###################################################################             FDB             ############################################################################################
############################################################################################################################################################################################
#Ця функція підключається до комутаторів, зберігає таблицю mac_address парсить та записує до файлів {switch_ip}_fdb.txt
# переменная в которой храниться дата создания конфига

              
def fdb():

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


############################################################################################################################################################################################
###################################################################             LEASE             ##########################################################################################
############################################################################################################################################################################################
#Ця функція підключається до DHCP серверу та зберігає dhcp lease до файлів {lease_ip}.csv

     

def lease():

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
            
            ssh.expect('[>]')
            ssh.sendline('powershell.exe')
            
            ssh.expect('[>]')
            
            for lease in Lease_list:
                ssh.sendline(r'Get-DhcpServerv4Lease -ScopeId {} | Select-Object -Property ClientId, IPAddress, HostName |  Export-Csv -Path C:\Users\Y.Kazabekov\{}.csv'.format(lease, lease))
            
            ssh.expect([pexpect.TIMEOUT, pexpect.EOF])
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
            
            ssh.expect('winscp>')
            ssh.sendline('exit')
            ssh.close()
        

############################################################################################################################################################################################
###################################################################             MYSQL UPDATER             ##################################################################################
############################################################################################################################################################################################

def dbupdater():
    
    
    ##############################################################################

    #ACSW_fdb = ['10.0.1.250_fdb.txt', '10.0.1.251_fdb.txt', '10.0.1.252_fdb.txt', '10.0.2.250_fdb.txt', '10.0.2.251_fdb.txt', '10.0.2.252_fdb.txt',  '10.0.3.250_fdb.txt', 
    #            '10.0.3.251_fdb.txt',   '10.0.3.252_fdb.txt', '10.0.3.253_fdb.txt', '10.0.4.250_fdb.txt', '10.0.4.251_fdb.txt', '10.0.4.252_fdb.txt',
    #            '10.0.5.250_fdb.txt', '10.0.5.251_fdb.txt', '10.0.5.252_fdb.txt', '10.0.5.253_fdb.txt','10.0.6.250_fdb.txt', '10.0.6.251_fdb.txt', '10.0.6.253_fdb.txt']


    result_array = []
    for file in ACSW_ip:
        switch_ip_address = file
        with open('/home/appliance/venv/parsed_fdb/'+ str(file) + '_fdb.txt') as file:
            array = [row.strip() for row in file]
            new_array = []
          
        for i in array:
            if 'Forward' in i and 'CPU' not in i:
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
    
    #text_sql = 'SELECT mac_address FROM fdb'
    #cursor.execute(text_sql)
    #result = cursor.fetchall()   

  
    for i in result_array:
        mac = i[2]
        text_sql = 'SELECT mac_address FROM fdb'
        cursor.execute(text_sql)
        result = cursor.fetchall() 
    #if mac in result:
        if any(mac in s for s in result):
        
            text_sql = 'DELETE FROM fdb WHERE mac_address = "{}"'.format(i[2])
            cursor.execute(text_sql) 
            text_sql = 'INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number, time_of_adding ) VALUES("{}",{},"{}","{}","{}")'.format(i[2],i[0], i[6], i[3], now.strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(text_sql)    
        else: 
            text_sql = 'INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number, time_of_adding ) VALUES("{}",{},"{}","{}","{}")'.format(i[2],i[0], i[6], i[3], now.strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(text_sql)
          
          
    ####################################################################################################################  LEASE
    text_sql = 'SELECT mac_address FROM lease'
    cursor.execute(text_sql)
    result = cursor.fetchall()


    Lease_list = ['10.0.1.0.csv', '10.0.2.0.csv', '10.0.3.0.csv', '10.0.4.0.csv','10.0.5.0.csv', '10.0.6.0.csv' ] 
    result_lease_array = []
    for file in Lease_list:
        with open('/home/appliance/venv/lease/'+file, 'rU') as f:  #opens PW file
            reader = csv.reader(f)
            data = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists

            for row in data:
                if row[0] == '#TYPE Selected.Microsoft.Management.Infrastructure.CimInstance' or row[0] == 'ClientId':
                    pass
                else:
                    result_lease_array.append(row)                  
                 
    for i in result_lease_array:
        try:  
            try:
                text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[0],i[1], i[2])
                cursor.execute(text_sql)
            except:
                text_sql = 'UPDATE lease SET IP=REPLACE("{}"), hostname=REPLACE("{}") WHERE mac_address="{}"'.format(i[1], i[2], i[0])        
                cursor.execute(text_sql)            
        except:
            pass          
            

#fdb()         
lease()
dbupdater()    
              
####################################################################################################################
text_sql = 'SELECT  fdb.mac_address, fdb.switch_IP, fdb.vlan_ID, lease.IP, lease.hostname, fdb.time_of_adding FROM fdb , lease  WHERE lease.mac_address = fdb.mac_address ORDER BY fdb.switch_IP'
cursor.execute(text_sql)
result = cursor.fetchall()

for x in result:
    print(x)
            
    


