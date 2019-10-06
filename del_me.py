import mysql.connector
from datetime import datetime
import csv 

now = datetime.now()
#formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')


    
conn = mysql.connector.connect(host='localhost',
                                  database='myapp',
                                  user='myapp',
                                  password='Mad_H0rse',
                                  autocommit=True)

cursor = conn.cursor()
##############################################################################

ACSW_fdb = ['10.0.1.250_fdb.txt', '10.0.1.251_fdb.txt', '10.0.1.252_fdb.txt', '10.0.2.250_fdb.txt', '10.0.2.251_fdb.txt', '10.0.2.252_fdb.txt',  '10.0.3.250_fdb.txt', 
			'10.0.3.251_fdb.txt',   '10.0.3.252_fdb.txt', '10.0.3.253_fdb.txt', '10.0.4.250_fdb.txt', '10.0.4.251_fdb.txt', '10.0.4.252_fdb.txt',
			'10.0.5.250_fdb.txt', '10.0.5.251_fdb.txt', '10.0.5.252_fdb.txt', '10.0.5.253_fdb.txt','10.0.6.250_fdb.txt', '10.0.6.251_fdb.txt', '10.0.6.253_fdb.txt']


result_array = []
for file in ACSW_fdb:
    switch_ip_address = file
    with open('/home/appliance/venv/parsed_fdb/'+ str(file)) as file:
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
            #i = ' '.join(i.split()) #Оставляет только один пробел
            final_array.append(i)         
            
            for item in final_array:
                a = item.split()
                
                mystring = str(switch_ip_address)
                keyword = '_fdb.txt'
                before_keyword, keyword, after_keyword = mystring.partition(keyword)
                mystring = before_keyword
                #keyword = '='
                #before_keyword, keyword, after_keyword = mystring.partition(keyword)
                #mystring = after_keyword  
                
                
                
                a.append(mystring)
                result_array.append(a)





for i in result_array:
    text_sql = 'SELECT mac_address FROM fdb'
    cursor.execute(text_sql)
    result = cursor.fetchall()
    for x in result:
       print(x)
    if i in result:
        print(i[2])
        text_sql = 'DELETE FROM fdb WHERE mac_address = "{}"'.format(i[2])
        cursor.execute(text_sql) 
        text_sql = 'INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number, time_of_adding ) VALUES("{}",{},"{}","{}","{}")'.format(i[2],i[0], i[6], i[3], now.strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(text_sql)    
    else: 
        #text_sql = 'INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number, time_of_adding ) VALUES("{}",{},"{}","{}","{}")'.format(i[2],i[0], i[6], i[3], now.strftime('%Y-%m-%d %H:%M:%S'))
        #cursor.execute(text_sql) 
        print('2222')
      
