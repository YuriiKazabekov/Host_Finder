import subprocess
import mysql.connector
import csv
from datetime import datetime


conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)

cursor = conn.cursor()

def adder():
    
    #file = input('Input filename')
    file = 'vms-07.csv'
    lines = []
    print(file)
    with open('/home/appliance/venv/lease/'+file, 'rU') as f:  #opens PW file

 
        for line in f: 
            line = line.strip() 
            lline = list(line.split("\t")) 
            if len(lline) == 3:
              
                mac = lline[1]
                print(mac)
                mac = mac[0:2] + '-' + mac[2:4] + '-' + mac[4:6] + '-' + mac[6:8] + '-' + mac[8:10] + '-' + mac[10:]
                lline[1] = mac
        
                lines.append(lline) 
       
       
    for i in lines:
        print(i)
    for i in lines:
        try:  
            text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[1],i[2], i[0])
            cursor.execute(text_sql)
        except:
            text_sql = 'DELETE FROM lease WHERE IP = "{}"'.format(i[2])
            cursor.execute(text_sql) 
            text_sql = 'DELETE FROM lease WHERE hostname = "{}"'.format(i[0])
            cursor.execute(text_sql)
            text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[1],i[2], i[0])
            cursor.execute(text_sql)  
            
            
            
adder()