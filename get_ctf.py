import sqlite3
DATABASE_CONNECTION = sqlite3.connect('data.db', check_same_thread=False)



cur = DATABASE_CONNECTION.cursor()	
for row in cur.execute('SELECT * FROM CTF'):
	print(row)
DATABASE_CONNECTION.commit()
DATABASE_CONNECTION.close()