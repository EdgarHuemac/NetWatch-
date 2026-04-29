import os
import glob
import sys
import traceback
import random, string
import uuid
import json
from datetime import datetime

import pickle
import sqlite3
from datetime import date, datetime
from flask import Flask, render_template, redirect, request, jsonify, url_for, abort, send_from_directory, make_response, session
from flask_session import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Sessions' configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf', '.JPG', '.txt']
app.config['UPLOAD_PATH'] = 'C:\\Users\\edgar\\Documents\\programming projects\\ctf-roadmap\\reports'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 50	# 50 Mb


DATABASE_CONNECTION = sqlite3.connect('data.db', check_same_thread=False)



def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row	
    return conn

def get_db_connection_administrators():
    conn = sqlite3.connect('administrator.db')
    conn.row_factory = sqlite3.Row	
    return conn    


def get_all_ctf():
	conn = get_db_connection()
	ctfs = conn.execute('SELECT * FROM CTF').fetchall()
	results = [tuple(row) for row in ctfs]
	print(results)
	conn.close()
	return ctfs

def get_all_user():
	conn = get_db_connection()
	users = conn.execute('SELECT * FROM USERS').fetchall()
	results = [tuple(row) for row in users]
	print(results)
	conn.close()
	return users	

def get_all_administrator():
	conn = get_db_connection_administrators()
	administrators = conn.execute('SELECT * FROM ADMINISTRATOR').fetchall()
	results = [tuple(row) for row in administrators]
	print(results)
	conn.close()
	return administrators	


def get_all_scans():
	conn = get_db_connection()
	scans = conn.execute('SELECT * FROM SCAN ORDER BY Time DESC').fetchall()
	results = [tuple(row) for row in scans]
	print(results)
	conn.close()
	return scans

def get_network_chart_data():
	conn = get_db_connection()
	scans = conn.execute('SELECT Time, AliveHosts FROM SCAN').fetchall()	# Return this for ServerSideRendering
	results = [tuple(row) for row in scans]	# Return this when JSON (ajax)
	conn.close()
	return results


# Reeturns ALL scan results
def get_all_scan_results():
	conn = get_db_connection()
	scan_results = conn.execute('SELECT * FROM SCAN_RESULT').fetchall()
	results = [tuple(row) for row in scan_results]
	print(results)
	conn.close()
	return scan_results	

# Reeturns only scan results from a SCAN
def get_scan_results_from_scan(scan_id):
	conn = get_db_connection()
	scan_results = conn.execute(f"""SELECT * FROM SCAN_RESULT where ScanId = '{scan_id}'""").fetchall()
	results = [tuple(row) for row in scan_results]
	print(results)
	conn.close()
	return results	

def check_administrator(username, password):
	conn = get_db_connection_administrators()
	administrators = conn.execute(f"""SELECT * FROM ADMINISTRATOR WHERE Username = '{username}' AND Password = '{password}'""").fetchall()
	results = [tuple(row) for row in administrators]
	conn.close()	
	#return json.dumps(results)
	return results



def create_user(id, name, mac, ip):
	try:
		sqliteConnection = sqlite3.connect('data.db')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")
		sqlite_insert_query = f"INSERT INTO USERS \
		(Id, Name, Mac, Ip)  \
		VALUES  \
		('{id}','{name}','{mac}','{ip}')"
		print(sqlite_insert_query)
		count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
		print("New user inserted successfully into data.db", cursor.rowcount)
		cursor.close()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print('Printing traceback')
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	finally:
		if sqliteConnection:
			sqliteConnection.close()


def create_administrator(id, name, username, password):
	try:
		sqliteConnection = sqlite3.connect('administrator.db')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")
		sqlite_insert_query = f"INSERT INTO ADMINISTRATOR \
		(Id, Name, Username, Password)  \
		VALUES  \
		('{id}','{name}','{username}','{password}')"
		print(sqlite_insert_query)
		count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
		print("New user inserted successfully into administrator.db", cursor.rowcount)
		cursor.close()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print('Printing traceback')
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	finally:
		if sqliteConnection:
			sqliteConnection.close()

def create_scan(agent_id, alive_hosts):
	scan_id = uuid.uuid4()
	scan_date = str(datetime.now().date())
	scan_time = str(datetime.now().time())
	scan_agent_id = agent_id
	try:
		sqliteConnection = sqlite3.connect('data.db')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")
		sqlite_insert_query = f"INSERT INTO SCAN \
		(Id, Date, Time, AgentId, AliveHosts)  \
		VALUES  \
		('{scan_id}','{scan_date}','{scan_time}','{scan_agent_id}', '{alive_hosts}')"
		print(sqlite_insert_query)
		count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
		print("New SCAN created successfully into data.db", cursor.rowcount)
		cursor.close()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print('Printing traceback')
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	finally:
		if sqliteConnection:
			sqliteConnection.close()
	return scan_id


def create_scan_result(scan_id, ip, mac, vendor):
	result_id = uuid.uuid4()
	result_scan_id = scan_id
	result_ip = ip
	result_mac = mac
	result_vendor = vendor
	try:
		sqliteConnection = sqlite3.connect('data.db')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")
		sqlite_insert_query = f"INSERT INTO SCAN_RESULT \
		(Id, ScanId, Ip, Mac, Vendor)  \
		VALUES  \
		('{result_id}','{result_scan_id}','{result_ip}','{result_mac}', '{result_vendor}')"
		print(sqlite_insert_query)
		count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
		print("New SCAN_RESULT created successfully into data.db", cursor.rowcount)
		cursor.close()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print('Printing traceback')
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	finally:
		if sqliteConnection:
			sqliteConnection.close()	



def create_ctf(reportId, name, platform, os, tools, techniques, reportName, ctfDatetime):		
	try:
		sqliteConnection = sqlite3.connect('data.db')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")

		sqlite_insert_query = f"INSERT INTO CTF \
		(Id, Name, Platform, Os, Tools, Techniques, ReportName, CtfDatetime)  \
		VALUES  \
		('{reportId}','{name}','{platform}','{os}', '{tools}', '{techniques}', '{reportName}', '{ctfDatetime}')"
		print(sqlite_insert_query)
		count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
		print("New ctf inserted successfully into data.db", cursor.rowcount)
		cursor.close()

	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print('Printing traceback')
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	finally:
		if sqliteConnection:
			sqliteConnection.close()

@app.route('/')
def index():
	users = get_all_user()	
	return render_template('index.html', users=users)

@app.route('/scan-results')
def scan_results():
	if not session.get("name"):        
		return redirect("/login")
	scan_results = get_all_scan_results()
	return render_template('scan-results.html', scan_results=scan_results)

@app.route('/scan-results-from-scan/<scan_id>')
def scan_results_from_scan(scan_id):
	if not session.get("name"):        
		return redirect("/login")
	scan_results = get_scan_results_from_scan(scan_id)
	return make_response(jsonify(scan_results), 201)

@app.route('/get-network-history')
def network_history():
	if not session.get("name"):        
		return redirect("/login")
	network_chart_data = get_network_chart_data()
	return make_response(jsonify(network_chart_data), 201)

@app.route('/scans')
def scans():
	if not session.get("name"):        
		return redirect("/login")
	scans = get_all_scans()
	return render_template('scans.html', scans=scans)

@app.route('/activity')
def activity():
	if not session.get("name"):        
		return redirect("/login")
	return render_template('activity.html')

@app.route('/new-administrator')
def new_administrator():
	if not session.get("name"):        
		return redirect("/login")
	administrators = get_all_administrator()	
	return render_template('new-administrator.html', administrators=administrators)

# return [ SELECT id,time from SCAN ]
def get_lista_s():
	query_statement = f"""SELECT Id, Time FROM SCAN"""
	print(f' ----------------- Executing: get_lista_s({query_statement})')
	conn = get_db_connection()
	query_results = conn.execute(query_statement).fetchall()
	results = [tuple(row) for row in query_results]	
	print(results)
	conn.close()
	return results

#return [ SELECT mac from SCAN_RESULT where mac = mac_target ]
def get_lista_sr(mac=None):
	query_statement = f"""SELECT Mac FROM SCAN_RESULT"""
	if mac and mac != None:
		query_statement = f"""SELECT ScanId, Mac FROM SCAN_RESULT WHERE Mac='{mac}'"""
	print(f'----------------- Executing statement: {query_statement}')	
	conn = get_db_connection()
	query_results = conn.execute(query_statement).fetchall()
	results = [tuple(row) for row in query_results]
	print(results)
	conn.close()
	return results

@app.route('/get-activity/<target_mac>')
def get_mac_activity(target_mac):
	if not session.get("name"):        
		return redirect("/login")
	target_mac = str(target_mac)
	if target_mac and target_mac != None:
		activity = []

		lista_s = get_lista_s()
		lista_sr = get_lista_sr(target_mac)			

		lista_s_id = [x[0] for x in lista_s]
		lista_sr_id = [x[0] for x in lista_sr]


		print('..............................')
		#print(lista_s)
		print(f">>> Checking network presence for: {target_mac} ")
		for s in lista_s_id:			
			if s in lista_sr_id:				
				activity.append( { "time": f"{lista_s[lista_s_id.index(s)][1]}", "state": "1" } )
				print(f'scanId={lista_s[lista_s_id.index(s)][0]} -- scanTime={lista_s[lista_s_id.index(s)][1]} : {s} ---> 1')
			else:				
				activity.append( { "time": f"{lista_s[lista_s_id.index(s)][1]}", "state": "0" } )
				print(f'scanId={lista_s[lista_s_id.index(s)][0]} -- scanTime={lista_s[lista_s_id.index(s)][1]} : {s} ---> 0')
		print('..............................')
		#for sr in lista_sr_id:
		#	print(sr)
		print('..............................')	
		
		#for k in lista_s:
		#	print(f"{k[0]} === {k[1]}")
		
		return make_response(jsonify(activity), 201)
	else:
		return make_response(jsonify('No MAC included'), 404)


@app.route('/get-ctf')
@app.route('/get-ctf/<ctf_id>')
def get_ctf_from_db(ctf_id='None'):
	if ctf_id == 'None':
		ctfs = get_all_ctf()
		data = []
		for ctf in ctfs:			
			data.append([x for x in ctf])
		return json.dumps(data), 200, {'Content-Type': 'json; charset=utf-8'}
	else:
		return get_single_ctf_bd(ctf_id), 200, {'Content-Type': 'json; charset=utf-8'}






@app.route('/login', methods=['GET', 'POST'])
def login():
	if session.get("name"):        
		return redirect("/scans")
	if request.method == "POST":
        # record the user name
        #session["name"] = request.form.get("name")
		username = request.form.get("username")
		password = request.form.get("password")
		res = check_administrator(username, password)
		res_list = list(res)	
		print(res_list)	
		if len(res_list) == 1:
			print(f'Starting new session as {res_list[0][2]}')
			session["name"] = res_list[0][2]
			return make_response(jsonify('success'), 201)
		else:
			return redirect("/login")        
		return redirect("/login")
	return render_template('login.html')


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/login")

# Register new user to monitor in networkl
@app.route('/register-user', methods=['POST'])
def register_user():
	print('Printing all parameters from request...')
	print(request.headers)
	reqForm = request.form
	
	user_id = uuid.uuid4()
	name = reqForm['userName']
	mac = reqForm['userMac']
	ip = reqForm['userIp']
	create_user(user_id, name, mac, ip)
	return 'Success!'



# Register new user to monitor in networkl
@app.route('/register-administrator', methods=['POST'])
def register_administrator():
	print('Printing all parameters from request...')
	print(request.headers)
	reqForm = request.form
	
	admin_id = uuid.uuid4()
	admin_name = reqForm['adminName']
	admin_username = reqForm['adminUsername']
	admin_password = reqForm['adminPassword']
	admin_password2 = reqForm['adminPassword2']
	create_administrator(admin_id, admin_name, admin_username, admin_password)
	return 'Success!'	

# Network scanning results data handler
@app.route('/register-network-scan', methods=['POST'])
def register_network_scan():	
	content = request.json
	dic_data = list(eval(str(content)))
	print(f" Hosts alive recieved ----------------> {len(dic_data)}")

	# First we create the object that represents the whole scan
	# we retrieve its id
	scan_id = create_scan('anonymous', len(dic_data))

	# Then, we create a new scan result for each result
	# and link it to the scan object by including the scan_id from above	
	for i in dic_data:
		print(f'Data: {i["ip"]} ---> {i["mac"]}')
		create_scan_result(scan_id, i["ip"], i["mac"], i["vendor"])
	return make_response(jsonify('Success! :D'), 201)




print(app.config)

if __name__ == '__main__':
	app.run(debug=True)
