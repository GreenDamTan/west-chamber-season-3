import socket,sys,random,errno,argparse,os
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

timeoutf = 0
resetf = 0

parser = argparse.ArgumentParser(description='gfw doser')
parser.add_argument('--action', default='', help='set to a if logging')
gOptions = parser.parse_args()
if gOptions.action == "a":
    timeoutf = open("status/timedout-ip.list", "a")
    resetf = open("status/refused-ip.list", "a")

ipm24set = {}
for ip in config.gConfig["BLOCKED_IPS"]:
    ipm24 = ".".join(ip.split(".")[:3])
    ipm24set[ipm24]=1

pid = os.getpid()
resetcnt = 0

while 1:
    ipm24list = ipm24set.keys()
    random.shuffle(ipm24list)

    for ipm24 in ipm24list:
        for last in range(1,256):
            oip = ipm24 + "." + str(last)
            if oip in badipset:
                #print "ignore", oip
                continue
            if oip in refusedipset:
                continue

            #print "connect to", oip
            try:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.settimeout(6)
                remote.connect((oip, 80))
                #remote.send("\r\n"*89)
                remote.send("\r\n\r\n" + "GET /theconnectionwasreset HTTP/1.1\r\nHost: twitter.com\r\n\r\n")
                remote.recv(1024*64)
                #print oip, "good"
                remote.close()
            except socket.timeout:
                badipset[oip]=1
                if timeoutf:
                    timeoutf.write(oip+"\n")
                    timeoutf.flush()
            except socket.error, e:
                #print oip, "socket.error", e
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

if timeoutf: timeoutf.close()
if resetf: resetf.close()
