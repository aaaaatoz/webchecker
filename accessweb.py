#this piece of code is to generate a presedu 'random' by time
import datetime
import urllib2

def getrandomnum():
	now = datetime.datetime.now()
	number = now.year+now.month+now.day+now.hour+now.minute
	return number%100

def accessweb(number):
	try:
		conn = urllib2.urlopen("http://ec2-54-252-170-169.ap-southeast-2.compute.amazonaws.com/proxy3/%d.html" %number,timeout=10)
		httpCode = conn.getcode()
		if httpCode == 200:
			response = conn.read()
	except Exception,e:
		pass
	finally:
		if conn:
			conn.close()	

if __name__=='__main__':
	accessweb(getrandomnum())
