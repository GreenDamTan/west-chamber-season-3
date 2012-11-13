#!/usr/bin/python

import socket,sys,random,errno,os
import config

def connectip(ip):
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote.settimeout(6)
    remote.connect((oip, 80))
    host = random.choice(config.gConfig["BLOCKED_DOMAINS_LIST"])
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
    import argparse
    parser = argparse.ArgumentParser(description='gfw doser')
    parser.add_argument('--action', default='', help='set to a if logging')
    gOptions = parser.parse_args()
except:
    class option:
        def __init__(self): 
            self.action = ''
    gOptions = option()

if gOptions.action == "c": #check
    timeoutf = open("status/timedout-ip-checked.list", "r")
    timeoutString = timeoutf.read()
    timeoutf.close()

    timeoutList = timeoutString.split("\n")
    
    timeoutf = open("status/timedout-ip-checked.list", "a")
    for oip in badipset:
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

if gOptions.action == "a": #append
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

            try:
                if gOptions.action == "a": print "connect to", oip
                connectip(oip)
            except socket.timeout:
                if timeoutf:
                    timeoutf.write(oip+"\n")
                    timeoutf.flush()
            except socket.error, e:
                if gOptions.action == "a": print oip, "socket.error", e

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
