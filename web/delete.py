import sqlite3
sqlite_file = '/home/appliance/venv/web/app.db'  
conn = sqlite3.connect(sqlite_file)
c = conn.cursor() 

c.execute("SELECT * FROM user")
all_rows = c.fetchall()
for row in all_rows:
    print(row)
 
username = input('Введитя имя пользователя которого вы хотите удалить') 

c.execute('DELETE FROM user WHERE username ="{}" '.format(username))

    
c.execute("SELECT * FROM user")
all_rows = c.fetchall()
for row in all_rows:
    print(row)
    
    
conn.commit()    
conn.close()