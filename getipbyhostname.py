import socket
import datetime
import MySQLdb as mdb
import sys

def getHOSTfromdb():
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		cur.execute("select hostname,productionIP,contingencyIP from DNSRecords")
		records = cur.fetchall()
	except mdb.Error, e:
    		sys.exit(1)
	finally:
    		if con:
        		con.close()
		return records

def writeDNSrecord(hostname,ip,status):
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		#cur.execute("select * from DNSRecords")
		insertstring = "insert into DNSchecklog(hostname,ip,status) values('%s','%s' ,'%s')" %(hostname,ip,status)
		cur.execute(insertstring)
		cur.execute('commit')
	except mdb.Error, e:
    		sys.exit(1)
	finally:
    		if con:
        		con.close()

def getIPByHostname(host):
	try:
		ip = socket.gethostbyname(host)
	except socket.gaierror:
		ip = ""
	return ip


if __name__=='__main__':
	log = open("/usr/local/webchecker/checklog.log",'a+')
	#for line in open(r'/usr/local/webchecker/hostname.conf'):
	records = getHOSTfromdb()
	for checkinfo in records:
		currentIP = getIPByHostname (checkinfo[0])
		time = str (datetime.datetime.now())
		if currentIP == checkinfo[1]:
			log.write(time+"\t"+"%s \t\tRunning on Production \t%s\n" %(checkinfo[0],currentIP))
			status = "production"
		elif currentIP == checkinfo[2]:
			log.write(time+"\t"+"%s \t\tRunning on Contingency \t%s\n" %(checkinfo[0],currentIP))
			status = "contingency"
		else:
			log.write(time+"\t"+"%s \t\tRunning on \t%s\n" %(checkinfo[0],currentIP))
			currentIP = "None"
			status = "none"
		log.flush()
		writeDNSrecord(checkinfo[0],currentIP,status)
	log.close()
		
			
		
