import mysql.connector
try:
    import mysql.connector
except:
    print('No library')
    
conn = mysql.connector.connect(host='localhost',
                                  database='myapp',
                                  user='myapp',
                                  password='Mad_H0rse',
                                  autocommit=True)
#print(type(conn))
cursor = conn.cursor()
#print(type(cursor))

text_sql = 'CREATE TABLE fdb (mac_address VARCHAR(20) PRIMARY KEY, vlan_ID VARCHAR(10), switch_IP VARCHAR(20), port_number VARCHAR(10), time_of_adding DATETIME, time_of_checking DATETIME)'
cursor.execute(text_sql)