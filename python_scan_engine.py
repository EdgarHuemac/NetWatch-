import nmap
from datetime import datetime
import requests
import json
import time
start_time = datetime.now()

SERVER = 'http://192.168.100.119:8088'
NETWORK = '192.168.100.0/24'
TIME_BETWEEN_SCANS = 3

def send_network_data(data):
	global SERVER
	json_data = json.dumps(data, indent = 4)
	print(json_data)
	r = requests.post(f'{SERVER}/register-network-scan', json=json_data)
	#print(r.json())
	print(r.status_code)

def scan_network():
	global NETWORK
	network = []
	nm = nmap.PortScanner()
	nm.scan(hosts=NETWORK, arguments='-sP')
	for ip in nm.all_hosts():
		host = nm[ip]
		mac = "-"
		vendorName = "-"
		if 'mac' in host['addresses']:
			mac = host['addresses']['mac']
			if mac in host['vendor']:
				vendorName = host['vendor'][mac]

		status = host['status']['state']
		rHost = {'ip': ip, 'mac': mac, 'vendor': vendorName, 'status': status}
		#print([rHost])
		network.append(rHost)
	return network

#hosts = scan_network()
#send_network_data(hosts)

while True:
    hosts = scan_network()
    send_network_data(hosts)
    time.sleep(TIME_BETWEEN_SCANS)

execution_time = datetime.now() - start_time
print(f"found {len(hosts)} hosts")
print(f"Execution time: {execution_time} sec")
