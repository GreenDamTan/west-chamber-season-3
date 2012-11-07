import socket,sys,random
import config

ipset = {}
badipset = {}

rf = open("timedout.list", "r")
blockedIpString = rf.read()
rf.close()

for ip in blockedIpString.split("\n"):
    badipset[ip]=1

rf = open("reset.list", "r")
resetIpString = rf.read()
rf.close()

for ip in resetIpString.split("\n"):
    ipset[ip]=1

wf = open("timedout.list", "a")
resetf = open("reset.list", "a")

while 1:
    for ip in config.gConfig["BLOCKED_IPS"]:
        ipm24 = ".".join(ip.split(".")[:3])
        for last in range(1,256):
            oip = ipm24 + "." + str(last)
            if oip in badipset:
                print "ignore", oip
                continue

            print "connect to", oip
            try:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.settimeout(3)
                remote.connect((oip, 80))
                #remote.send("\r\n"*89)
                remote.send("\r\n"*random.randint(64,89) + "GET /theconnectionwasreset HTTP/1.1\r\n")
                print oip, "good: ", len(remote.recv(1024*1024))
                remote.close()
            except socket.timeout:
                badipset[oip]=1
                wf.write(oip+"\n")
                wf.flush()
            except:
                print oip, "bad", sys.exc_info()
                if oip in ipset:
                    continue

                ipset[oip]=1
                resetf.write(oip+"\n")
                resetf.flush()


wf.close()
resetf.close()
