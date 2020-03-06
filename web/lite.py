import sqlite3
sqlite_file = '/home/appliance/venv/web/app.db'  
conn = sqlite3.connect(sqlite_file)
c = conn.cursor() 
c.execute("SELECT * FROM user")
all_rows = c.fetchall()
for row in all_rows:
    print(row)
    
    
c.query(user).filter(user.username=='test')
