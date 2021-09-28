from scapy.all import *

def getByIPRange(suppliedIP, startIP=1, endIP=254):
    pos = 0
    while pos != -1:
        lastpos = pos
        pos = suppliedIP.find(".", pos+1, len(suppliedIP))

    cutIP = suppliedIP[:lastpos]

    for x in range(startIP,endIP):

        ipToUse = f"{cutIP}.{x}"
        print(f"at: {ipToUse}")

        packet = IP(dst=ipToUse)/ICMP()
        res = sr1(packet, timeout=0.05)

        if res is not None:
            print(f"{ipToUse} reachable, trying DNSQR!")
            
            dns_resp = sr1(IP(dst=ipToUse) / UDP(dport=53) /
               DNS(rd=1, qd=DNSQR(qname="google.com")), timeout=0.05)

            if dns_resp is not None:
                for x in range(dns_resp[DNS].ancount):
                    print(f"Found DNS Server at: {ipToUse}")
                    return ipToUse
        else:
            print("Destination Unreachable!")
    return False