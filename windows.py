import os
import sys
import random, string
from datetime import datetime


def get_firewall_displayname():
	now = datetime.now()
	dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
	random_numchar = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
	dt_string += f'_{random_numchar}'
	return dt_string

def blacklist_powershell(ip_to_block):	
	try:
		firewall_rule = f'New-NetFirewallRule -DisplayName "rule_{get_firewall_displayname()}" -Direction Outbound –LocalPort Any -Protocol TCP -Action Block -RemoteAddress {ip_to_block}'
		print(firewall_rule);
	except Exception as e:
		print("Blacklisting exception ", e.__class__, " occurred.")


blacklist_powershell('10.10.11.2')		