import socket
import datetime
import MySQLdb as mdb
import sys
import urllib2

def getURLfromdb():
	try:
		con = mdb.connect('localhost', 'webchecker', '', 'monitor');
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
	"""
	try:
		httpCode = -1
		conn = urllib2.urlopen(url,timeout=10)
		httpCode = conn.getcode()
		if httpCode == 200:
			response = conn.read()
			if outagekeyword in response:
				status = 'outage'
			elif keyword in response:
				status = 'production'
			else:
				status = 'error'
		else:
			status = "error"
	except Exception,e:
		status = "error"
	finally:
		if conn:
			conn.close()
		return httpCode, status

def writeURLrecord(url,httpCode,status):
	try:
		con = mdb.connect('localhost', 'webchecker', '', 'monitor');
		cur = con.cursor()
		insertstring = "insert into URLchecklog(url,returncode,status) values('%s','%d' ,'%s')" %(url,httpCode,status)
		cur.execute(insertstring)
	except mdb.Error, e:
		print "here"
		sys.exit(1)
	finally:
		if con:
			con.close()

if __name__=='__main__':
	records = getURLfromdb()
	for record in records:
		httpCode, status = getURLstatus(record[0],record[1],record[2])
		writeURLrecord(record[0],httpCode,status)
