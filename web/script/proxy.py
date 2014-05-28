#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
import flup.server.fcgi as flups  
import MySQLdb as mdb

import threading
import time

class ProxyProbing(threading.Thread):
        def __init__(self,proxyname):
                threading.Thread.__init__(self)
                self.proxyname = proxyname
                self.counter = 0

        def noProxyProbe(self):
                sqlstatement = "insert into PROXYchecklog (proxyname,status) values('%s','missing')" %self.proxyname
                try:
                        con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
                        cur = con.cursor()
                        cur.execute(sqlstatement)
                        cur.execute('commit')
                except mdb.Error, e:
                        pass
                finally:
                        if con:
                                con.close()
	def resetCounter(self):
		self.counter = 0

        def run(self):
                while True:
                        if self.counter >= 675:
                                self.counter = 0
                                self.noProxyProbe()
                        else:
                                self.counter += 1
                        time.sleep(1)

def insertproxy(proxy):
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		sqlstatement = "insert into PROXYchecklog(proxyname,status) values ('%s','hitted')" %proxy
		cur.execute(sqlstatement)
		cur.execute('commit')
	except mdb.Error, e:
		pass
	finally:
		if con:
			con.close()
  
def application(environ, start_response):  
	ret = ""  
	global proxy
	try:  
		uri = environ['PATH_INFO']  
		if uri == "/proxy3-corp" :
			insertproxy(uri[1:])
			proxy3.resetCounter()
		if uri == "/proxy4-corp" :
			insertproxy(uri[1:])
			proxy4.resetCounter()
		if uri == "/proxy-corp" :
			insertproxy(uri[1:])
			proxy.resetCounter()
		ret = "Good"
	except Exception, e:  
		ret = str(e)  
	status = '200 OK'  
	response_headers = [('Content-type','text/plain')]  
	start_response(status, response_headers)  
	return [ret]  
  
if __name__ == "__main__":  
	proxy3 = ProxyProbing("proxy3-corp")
	proxy3.start()
	proxy4 = ProxyProbing("proxy4-corp")
	proxy4.start()
	proxy = ProxyProbing("proxy-corp")
	proxy.start()
	flups.WSGIServer(application).run()
