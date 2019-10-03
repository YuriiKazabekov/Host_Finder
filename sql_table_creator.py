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

#text_sql = 'CREATE TABLE fdb (mac_address VARCHAR(20) PRIMARY KEY, vlan_ID VARCHAR(10), switch_IP VARCHAR(20), port_number VARCHAR(10), time_of_adding DATETIME)'
#text_sql = 'CREATE TABLE lease (mac_address VARCHAR(100) PRIMARY KEY, IP VARCHAR(100), hostname VARCHAR(100))'
#cursor.execute(text_sql)

#text_sql = 'DROP TABLE lease'
#cursor.execute(text_sql)
#text_sql = 'DROP TABLE fdb'
#cursor.execute(text_sql)
text_sql = 'CREATE TABLE fdb (mac_address VARCHAR(100) PRIMARY KEY NOT NULL, vlan_ID VARCHAR(100), switch_IP VARCHAR(100), port_number VARCHAR(20), time_of_adding DATETIME)'
cursor.execute(text_sql)
text_sql = 'CREATE TABLE lease (mac_address VARCHAR(100) , IP VARCHAR(100) PRIMARY KEY NOT NULL, hostname VARCHAR(100))'#cursor.execute(text_sql)
cursor.execute(text_sql)

#text_sql = 'INSERT INTO fdb (mac_address , vlan_ID , switch_IP , port_number , time_of_hecking) VALUES("00-17-C8-77-A5-DB", "101", "10.0.1.251", "1:3")'
#text_sql = 'INSERT INTO fdb (mac_address , vlan_ID , switch_IP , port_number ) VALUES("00-17-C8-77-A5-DB", "101", "10.0.1.251", "1:3")'
#text_sql = 'INSERT INTO fdb (mac_address , vlan_ID , switch_IP , port_number ) VALUES("00-CC-CC-77-AA-CC", "102", "10.0.1.251", "1:5")'
#text_sql = "INSERT INTO fdb(mac_address , vlan_ID , switch_IP , port_number ) VALUES({0},{1},{2})".format(mac_address, vlan_ID, data_type)
#cursor.execute(text_sql)


#text_sql = 'UPDATE fdb SET vlan_ID="000", switch_IP="00.0.0.000", port_number="0:0" WHERE mac_address="00-CC-CC-77-AA-CC"'

#cursor.execute(text_sql)


'''text_sql = 'SELECT * FROM lease'
cursor.execute(text_sql)
result = cursor.fetchall()

for x in result:
    print(x)

cursor.execute("SHOW TABLES")
for x in cursor:
    print(x)


text_sql = 'SELECT * FROM fdb'
cursor.execute(text_sql)
result = cursor.fetchall()

for x in result:
    print(x)'''
