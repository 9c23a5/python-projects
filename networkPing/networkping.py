import ipaddress
import sys
import re
import subprocess

if sys.platform == "win32":
  ping_count = "-n"
  ping_timeout = "-w"
elif sys.platform in ["linux", "linux2"]:
  ping_count = "-c"
  ping_timeout = "-W"

class color:
  RED = '\033[91m'
  GREEN = '\033[92m'
  END = '\033[0m'

error_msg = 'Please enter your network in CIDR format'

def ping_ips(ip_list):
  class returnObject:
    ip_ok = []
    ip_err = []
  
  for ip in ip_list:
    ip = str(ip)
    ping_command = (["ping", ping_count, "1", ping_timeout, "1", ip])
    ping = subprocess.run(args=ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    if ping == 0:
      print(f"{ip}\t{color.GREEN}OK!{color.END}")
      returnObject.ip_ok.append(ip)
    else:
      print(f"{ip}\t{color.RED}ERROR{color.END}")
      returnObject.ip_err.append(ip)
    
  return returnObject

if len(sys.argv) == 1:
  print(error_msg)
  exit(1)

user_input = sys.argv[1]

validip = re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/([0-9]|[0-2][0-9]|3[0-2])$",user_input)

try:
  cidr = validip.group()
except:
  print(error_msg)
  exit(2)

try:
  ip_list = list(ipaddress.IPv4Network(cidr).hosts())
except:
  print(error_msg)
  exit(3)

print(f"Pinging every IP in {cidr}")

confirmed = False
while not confirmed:
  print(f"There are {len(ip_list)} IPs in this network, do you wish to continue?")
  user_input = input().lower()
  if user_input in ["n", "no"]:
    print("User cancelled operation")
    exit(100)
  elif user_input in ["y", "yes"]:
    confirmed = True
  else:
    continue

result = ping_ips(ip_list)
