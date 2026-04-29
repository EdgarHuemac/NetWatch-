import sqlite3
 
# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('data.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS CTF")
 
# Creating table
table = """ CREATE TABLE CTF (
            Id TEXT,
            Name TEXT,
            Platform TEXT,
            Os TEXT,
            Tools TEXT,
            Techniques TEXT,
            ReportName TEXT,
            CtfDatetime TEXT
        ); """
 
cursor_obj.execute(table)
 
print("Table CTF is Ready")
 
# Close the connection
connection_obj.close()