#!/usr/bin/python
#using scapy to inject ack
#but scapy lock resource, buggy

import socket,sys,random,errno,os,threading
import config

sending = 0
class sendSYN(threading.Thread):
    dstIP = ""
    def __init__(self, dst):
        global sending
        threading.Thread.__init__(self)
        print "sending ack " + dst +" " + str(sending)
        sending += 1
        self.dstIP = dst

    def run(self):
        from scapy.all import *
        global sending
        conf.iface='en0';#network card XD

        t = TCP()
        t.sport = random.randint(1,65535)
        t.dport = 80
        t.flags = 'A'
        t.payload = "GET / HTTP/1.1\r\nHost: twitter.com\r\n\r\n"

        sendp(Ether(type=0x800) / IP(dst=self.dstIP) / t, verbose=0)
        sending -= 1
        print "sent ack " + self.dstIP

def connectip(ip):
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote.settimeout(6)
    remote.connect((oip, 80))
    #host = random.choice(config.gConfig["BLOCKED_DOMAINS_LIST"])
    host = "twitter.com"
    remote.send("GET / HTTP/1.1\r\nHost: "+host+"\r\n\r\n")
    remote.recv(1024*64)
    #print oip, "good"
    remote.close()

refusedipset = {}
badipset = {}

rf = open("status/timedout-ip.list", "r")
blockedIpString = rf.read()
rf.close()

for ip in blockedIpString.split("\n"):
    if len(ip) >= 7:
        badipset[ip]=1

rf = open("status/refused-ip.list", "r")
resetIpString = rf.read()
rf.close()

for ip in resetIpString.split("\n"):
    if len(ip) >= 7: 
        refusedipset[ip]=1

timeoutf = 0
resetf = 0

try:
    class option:
        def __init__(self): 
            self.action = ''
            self.verbose = 0
    gOptions = option()
    if len(sys.argv) >= 2:
        gOptions.action = sys.argv[1]
    if len(sys.argv) >= 3:
        gOptions.verbose = sys.argv[2]
except:
    print "usage: ./dos.py <action> <verbose>"
    
if gOptions.action == "c": #check
    timeoutf = open("status/timedout-ip-checked.list", "r")
    timeoutString = timeoutf.read()
    timeoutf.close()

    timeoutList = timeoutString.split("\n")
    
    timeoutf = open("status/timedout-ip-checked.list", "a")
    for oip in badipset:
        oip = oip.split(" ")[0]
        if oip in timeoutList:
            print "ignore ", oip
            continue

        print "connect to", oip
        try:
            connectip(oip)
        except socket.timeout:
            print "timed out", oip
            timeoutf.write(oip+"\n")
            timeoutf.flush()
        except:
            print "connected to", oip
    timeoutf.close()
    exit(0)

verbose = gOptions.verbose
pid = os.getpid()
if gOptions.action == "a": #append
    timeoutf = open("status/timedout-ip.list"+".pid"+str(pid), "a")
    resetf = open("status/refused-ip.list", "a")
    verbose = 1

ipm24set = {}
for ip in config.gConfig["BLOCKED_IPS"]:
    ipm24 = ".".join(ip.split(".")[:3])
    ipm24set[ipm24]=1
for ip in config.gConfig["BLOCKED_IPS_M24"]:
    ipm24set[ip] = 1
    if verbose: print "M24: " + ip

for ip in config.gConfig["BLOCKED_IPS_M16"]:
    for ip3 in range(256):
        ipm24 = ip + "." + str(ip3)
        ipm24set[ipm24]=1
        if verbose: print "M16: " + ipm24

resetcnt = 0

while 1:
    ipm24list = ipm24set.keys()
    random.shuffle(ipm24list)

    for ipm24 in ipm24list:
        for last in range(1,256):
            oip = ipm24 + "." + str(last)
            if oip in badipset:
                if sending < 8: sendSYN(oip).start()
                continue
            if oip in refusedipset:
                if sending < 8: sendSYN(oip).start()
                continue

            try:
                if verbose: print "connect to", oip
                connectip(oip)
            except socket.timeout:
                if sending < 8: sendSYN(oip).start()
                if timeoutf:
                    timeoutf.write(oip+"\n")
                    timeoutf.flush()
            except socket.error, e:
                if verbose: print oip, "socket.error", e

                if e[0] == errno.ECONNRESET:
                    resetcnt += 1
                    #print "*" resetcnt, "resets"
                    if resetcnt % 100 == 0:
                        print pid, resetcnt, "resets"
                        continue
                if e[0] == errno.ECONNREFUSED:
                    #print "* refused", oip
                    refusedipset[oip]=1
                    if resetf:
                        resetf.write(oip+"\n")
                        resetf.flush()

    if gOptions.action == "a": #append
        break

if timeoutf: timeoutf.close()
if resetf: resetf.close()
