# -*- coding: utf-8 -*-
# author: liruqi@gmail.com

import asyncore, socket, sys, urlparse, threading, time, random
from httplib import HTTPResponse

#收到data最大長度
MAX_RECV = 4096
gConfig = {}

#等待server傳送訊息的thread
class send_server_thread(threading.Thread):
    def __init__(self,ip,port):
        print "init " + ip
        #self.client = client(ip,port)
        self.ip = ip
        self.port = port
        self.error = 0
        self.status = 0
        self.clientSendData = ""
        self.clientRecvData = ""
        threading.Thread.__init__ ( self )
        
    def run(self):
        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((self.ip, int(port)))
            remote.send(self.clientSendData)
            response = HTTPResponse(remote)
            response.begin()
            for hh, vv in response.getheaders():
                if hh.upper()!='TRANSFER-ENCODING':
                    self.clientRecvData += hh + ': ' + vv + '\r\n'

            self.clientRecvData += "\r\n"
            self.status = response.status
            print (self.ip + " response: %d"%(response.status))
            while True:
                d = remote.recv(MAX_RECV)
                if (len(d)==0): break
                self.clientRecvData += d
            
        except:
            exc_type, self.error, exc_traceback = sys.exc_info()
            print (self.ip+":"+self.port + " error: " , exc_type , self.error)
            sys.stdout.flush()


#主程式
if __name__ == "__main__":
    s = open("../west-chamber-proxy/httpproxy.list")
    gConfig["HTTP_PROXY_SERVERS"] = []
    threads = []
    socket.setdefaulttimeout(6)
    url = "http://twitter.com/"
    if len(sys.argv) > 1: url=sys.argv[1]
        
    (scm, netloc, path, params, query, _) = urlparse.urlparse(url)
    if path=="": path="/"
    for line in s.readlines():
        line = line.strip()
        ip, port = line.split(':')
        client_thread = send_server_thread(ip, port)
        gConfig["HTTP_PROXY_SERVERS"].append((ip,(int)(port)))

        if random.randint(0,3) != 0: continue
 
        print (scm, netloc, path, params, query)
        #client_thread.client.SendData = (" ".join(("GET", path, "1.1")) + "\r\n") + "Host: " + netloc + "\r\n" + "\r\n"
        client_thread.clientSendData = (" ".join(("GET", path, "1.1")) + "\r\n") + "Host: " + netloc + "\r\n" + "\r\n"
        
        client_thread.start()
        threads.append(client_thread)

    time.sleep(6)
    print ("Check recv data.")
    recvset = {}
    """
    for thread in threads:
        if len(thread.client.RecvData) > 0:
            if thread.client.RecvData in recvset:
                recvset[thread.client.RecvData] += 1
            else:
                recvset[thread.client.RecvData] = 1
    """
    ef = open(netloc+".log", "w")
    for thread in threads:
        if len(thread.clientRecvData) > 0:
            if thread.status == 200:
                ef.write ("200: " + thread.ip + thread.clientRecvData)
                continue
            if thread.clientRecvData in recvset:
                recvset[thread.clientRecvData] += 1
            else:
                recvset[thread.clientRecvData] = 1
            #thread.exit()

    recvmax = ""
    recvmaxcnt = 0
    for data in recvset:
        if recvset[data] > recvmaxcnt:
            recvmaxcnt = recvset[data] 
            recvmax = data

    ef.write("Error: " + recvmax)
    ef.close()
    exit(1)

