import sqlite3
 
# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('data.db')
 
# cursor object
cursor_obj = connection_obj.cursor()

# Creating table 'CTF'
cursor_obj.execute("DROP TABLE IF EXISTS CTF")
ctf_table = """ CREATE TABLE CTF (
            Id TEXT,
            Name TEXT,
            Platform TEXT,
            Os TEXT,
            Tools TEXT,
            Techniques TEXT,
            ReportName TEXT,
            CtfDatetime TEXT
        ); """

cursor_obj.execute(ctf_table)
print("Table 'CTF' created succesfully!")



# Creating table 'TOOLS_TRICKS'
cursor_obj.execute("DROP TABLE IF EXISTS TOOLS_TRICKS")
ctf_table = """ CREATE TABLE TOOLS_TRICKS (
            Id TEXT,
            CtfId TEXT,
            Command TEXT,
            Description TEXT            
        ); """

cursor_obj.execute(ctf_table)
print("Table 'TOOLS_TRICKS' created succesfully!")



# Creating table 'USERS'
cursor_obj.execute("DROP TABLE IF EXISTS USERS")
users_table = """ CREATE TABLE USERS (
            Id TEXT,
            Name TEXT,
            Mac TEXT,
            Ip TEXT            
        ); """
cursor_obj.execute(users_table)
print("Table 'USERS' created succesfully!")


# Creating table 'SCAN'
cursor_obj.execute("DROP TABLE IF EXISTS SCAN")
scan_table = """ CREATE TABLE SCAN (
            Id TEXT,
            Date TEXT,
            Time TEXT,
            AgentId TEXT, 
            AliveHosts TEXT
        ); """
cursor_obj.execute(scan_table)
print("Table 'SCAN' created succesfully!")


# Creating table 'SCAN_RESULT'
cursor_obj.execute("DROP TABLE IF EXISTS SCAN_RESULT")
scan_result_table = """ CREATE TABLE SCAN_RESULT (
            Id TEXT,
            ScanId TEXT,            
            Ip TEXT, 
            Mac TEXT,
            Vendor TEXT
        ); """
cursor_obj.execute(scan_result_table)
print("Table 'SCAN_RESULT' created succesfully!")


# Creating table 'ADMINISTRATOR'
administrator_connection_obj = sqlite3.connect('administrator.db')
administrator_cursor_obj = administrator_connection_obj.cursor()
administrator_cursor_obj.execute("DROP TABLE IF EXISTS ADMINISTRATOR");
administrator_table = """ CREATE TABLE ADMINISTRATOR (
    Id TEXT, 
    Name TEXT, 
    Username TEXT, 
    Password TEXT
);"""
administrator_cursor_obj.execute(administrator_table)
print("Table 'ADMINISTRATOR' created succesfully!")

connection_obj.close()
