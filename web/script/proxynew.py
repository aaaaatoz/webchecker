import threading
import time
import MySQLdb as mdb

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

	def run(self):
		while True:
			if self.counter >= 61:
				self.counter = 0
				self.noProxyProbe()
			else:
				self.counter += 1
			time.sleep(1)

if __name__ == "__main__":
	proxy3 = ProxyProbing("proxy3-corp")
	proxy3.start()
