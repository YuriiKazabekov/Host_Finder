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

    result_lease_array = []
    #file = input('Input filename')
    file = 'VMHostNetworkDetails.csv'
    print(file)
    with open('/home/appliance/venv/lease/'+file, 'rU') as f:  #opens PW file
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader((line.replace('"', '') for line in f), delimiter=',')) #reads csv into a list of lists
        print(data)
        for row in data:
            if row[0] == '#TYPE Selected.VMware.VimAutomation.ViCore.Impl.V1.Host.Networking.Nic.PhysicalNicImpl' or row[0] == '"VMHost"':
                pass
            else:
                result_lease_array.append(row)  
                
    print(result_lease_array)            
    
    for i in result_lease_array:
        try:  
            text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[4],i[2], i[0]+"_"+i[1])
            cursor.execute(text_sql)
        except:
            text_sql = 'DELETE FROM lease WHERE IP = "{}"'.format(i[2])
            cursor.execute(text_sql) 
            text_sql = 'DELETE FROM lease WHERE hostname = "{}"'.format(i[0]+i[1])
            cursor.execute(text_sql)
            text_sql = 'INSERT INTO lease(mac_address , IP, hostname ) VALUES("{}","{}","{}")'.format(i[4],i[2], i[0]+"_"+i[1])
            cursor.execute(text_sql)  
            
            
            
adder()