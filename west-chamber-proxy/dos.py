import socket,sys,random,errno
import config


refusedipset = {}
badipset = {}

rf = open("status/timedout-ip.list", "r")
blockedIpString = rf.read()
rf.close()

for ip in blockedIpString.split("\n"):
    badipset[ip]=1

rf = open("status/refused-ip.list", "r")
resetIpString = rf.read()
rf.close()

for ip in resetIpString.split("\n"):
    refusedipset[ip]=1

wf = open("status/timedout-ip.list", "a")
resetf = open("status/refused-ip.list", "a")

while 1:
    for ip in config.gConfig["BLOCKED_IPS"]:
        ipm24 = ".".join(ip.split(".")[:3])
        for last in range(1,256):
            oip = ipm24 + "." + str(last)
            if oip in badipset:
                #print "ignore", oip
                continue
            if oip in refusedipset:
                continue

            print "connect to", oip
            try:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.settimeout(6)
                remote.connect((oip, 80))
                #remote.send("\r\n"*89)
                remote.send("\r\n\r\n" + "GET /theconnectionwasreset HTTP/1.1\r\nHost: twitter.com\r\n\r\n")
                remote.recv(1024*64)
                print oip, "good"
                remote.close()
            except socket.timeout:
                badipset[oip]=1
                wf.write(oip+"\n")
                wf.flush()
            except socket.error, e:
                print oip, "socket.error", e
                
                if e[0] == errno.ECONNREFUSED:
                    print "* refused", oip
                    refusedipset[oip]=1
                    resetf.write(oip+"\n")
                    resetf.flush()

wf.close()
resetf.close()
