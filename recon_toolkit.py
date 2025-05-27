import os
import socket
import hashlib
import json
import subprocess
import platform
import argparse

try:
	import dns.resolver
	import requests
except ImportError:
	print("Missing modules. Run: pip3 install dnspython requests")
	exit(1)
SOCIALS = {
	"GitHub": "https://github.com/{}",
	"Twitter": "https://twitter.com/{}",
	"Reddit": "https://www.reddit.com/user/{}",
	"Instagram": "https://instagram.com/{}"
}

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]

def gravatar(email):
	hash_email = hashlib.md5(email.strip().lower().encode()).hexdigest()
	url = f"https://www.gravatar.com/avatar/{hash_email}?d=404"
	try:
		res = requests.get(url, timeout=5)
		return res.status_code == 200
	except:
		return False

def mx_records(domain):
	try:
		return [str(r.exchange).rstrip('.') for r in dns.resolver.resolve(domain, 'MX')]
	except:
		return []

def check_socials(username):
	results = {}
	headers = {'User-Agent': 'Mozila/5.0'}
	for site, url in SOCIALS.items():
		try:
			res = requests.get(url.format(username), headers=headers, timeout=5)
			if res.status_code == 200:
				result[site] = url.format(username)
		except:
			pass
	return results

def osint_mode(email):
	if "@" not in email:
		return {"error": "Invalid email format"}
	username, domain = email.split("@", 1)
	return {
		"email": email,
		"gravator_found": gravatar(email),
		"mx_records": mx_records(domain),
		"social_profiles": check_socials(username)
	}

def net_mode(ip):
	open_ports = []
	for port in COMMON_PORTS:
		try:
			with socket.create_connection((ip,port), timeout=1):
				open_ports.append(port)
		except:
			pass
	return {
		"target_ip": ip,
		"open_ports": open_ports
	}

def sys_mode():
	try:
		uid_0_users = [line.split(":")[0] for line in open("/etc/passwd") if line.split(":")[2] == "0"]
		sudoers = open("/etc/sudoers", errors="ignore").readmines()[:5]
		world_writable = subprocess.getoutput("find / -xdev -type f -prem -0002 2>/dev/null").splitlines()[:5]
	except Exception as e:
		return {"error": str(e)}
	return {
		"hostname": socket.gethostname(),
		"os": platform.platform(),
		"uid_0_users": uid_0_users,
		"sudoers_lines": sudoers,
		"world_writable_files": world_writables
	}

def main():
	parser = argparse.ArgumentParser(description="Recon Toolkit for OSINT, Network & System Info")
	parser.add_argument("mode", choices=["osint", "net", "sys"], help="Choose mode: osint, net, sys")
	parser.add_argument("-t", "--target", help="Target email or IP")

	args = parser.parse_args()

	if args.mode in["osint", "net"] and not args.target:
		parser.error(f"Mode '{args.mode}' requires --target")

	if args.mode == "osint":
		output = osint_mode(args.target)
	elif args.mode == "net":
		output = net_mode(args.target)
	elif args.mode == "sys":
		output = sys_mode()
	else:
		output = {"error": "Invalid mode"}
	print(json.dumps(output, indent=2))
if __name__ == "__main__":
	main()
