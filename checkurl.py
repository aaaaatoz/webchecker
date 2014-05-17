import socket
import datetime
import MySQLdb as mdb
import sys
import urllib2

def getURLfromdb():
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		cur.execute("select url,keywords,outagekeyword from URLRecords where checked = true")
		records = cur.fetchall()
	except mdb.Error, e:
     		sys.exit(1)
	finally:
     		if con:
			con.close()
	return records

def getURLstatus(url,keyword,outagekeyword):		
	""" the function to check if the URL is working
	input: 	url - http URL
			keyword - the keyword to search
			outagekeyword - check if the url contains the outage information
	return httpCode, status and timeused,
	"""
	try:
		httpCode = -1
		timeused = -1
		timestamp1 = datetime.datetime.now()
		conn = urllib2.urlopen(url,timeout=10)
		httpCode = conn.getcode()
		if httpCode == 200:
			response = conn.read()
			timestamp2 = datetime.datetime.now()
			if outagekeyword in response:
				status = 'outage'
			elif keyword in response:
				status = 'production'
			else:
				status = 'error'
			timeused = (timestamp2-timestamp1).seconds+(timestamp2-timestamp1).microseconds/1000000.0
		else:
			status = "error"
	except Exception,e:
		status = "error"
	finally:
		if conn:
			conn.close()
		return httpCode, status, timeused

def writeURLrecord(url,httpCode,status,timeused):
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		insertstring = "insert into URLchecklog(url,returncode,status,timeused) values('%s','%d' ,'%s','%.6f')" %(url,httpCode,status,timeused)
		cur.execute(insertstring)
		cur.execute('commit')
	except mdb.Error, e:
		print "here"
		sys.exit(1)
	finally:
		if con:
			con.close()

if __name__=='__main__':
	records = getURLfromdb()
	for record in records:
		httpCode, status, timeused = getURLstatus(record[0],record[1],record[2])
		writeURLrecord(record[0],httpCode,status,timeused)
