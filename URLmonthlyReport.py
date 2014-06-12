import datetime
import sys
import MySQLdb as mdb
import boto
import boto.s3.connection

def moveRecords():
	try:
		now=datetime.datetime.now()
		firstDayOfMonth = "-".join([str(now.year),str(now.month),'01'])
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		sqlstatement = "set autocommit=0"
		cur.execute(sqlstatement)
		sqlstatement = r"insert into URLchecklogArchiver(id,timestamp,url,returncode,status,timeused) select id,timestamp,url,returncode,status,timeused from URLchecklog where timestamp < '"+ firstDayOfMonth+"'"
		cur.execute(sqlstatement)
		sqlstatement = "delete from URLchecklog where timestamp < '"+ firstDayOfMonth+"'"
		cur.execute(sqlstatement)
		con.commit()
	except mdb.Error, e:
		print "Error"
		sys.exit(1)
	finally:
		if con:
			con.close()

def getURLfromdb():
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor');
		cur = con.cursor()
		cur.execute("select url from URLRecords where checked = true")
		records = cur.fetchall()
	except mdb.Error, e:
		sys.exit(1)
	finally:
		if con:
			con.close()
	return records

def getURLMonthlyReport(url):
	now=datetime.datetime.now()
	firstDayOfMonth = "-".join([str(now.year),str(now.month),'01'])
	allCountSQL = r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "'";
	prodCountSQL = r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "' and status = 'production'";
	outageCountSQL = r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "' and status = 'outage'";
	errorCountSQL = r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "' and status = 'error'";
	_1sCountSQL =  r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "' and timeused < 1.0 ";
	_5sCountSQL =  r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "' and timeused < 5.0 and timeused >= 1.0";
	longCountSQL = r"select count(*) from URLchecklog where timestamp < '" + firstDayOfMonth + "' and url = '" + url+ "' and timeused >= 5.0 ";
	try:
		con = mdb.connect('localhost', 'webchecker', 'rms', 'monitor')
		cur = con.cursor()
		cur.execute(allCountSQL)
		allCount = cur.fetchall()[0][0]
		cur.execute(prodCountSQL)
		prodCount = cur.fetchall()[0][0]
		cur.execute(outageCountSQL)
		outageCount = cur.fetchall()[0][0]
		cur.execute(errorCountSQL)
		errorCount = cur.fetchall()[0][0]
		cur.execute(_1sCountSQL)
		_1sCount = cur.fetchall()[0][0]
		cur.execute(_5sCountSQL)
		_5sCount = cur.fetchall()[0][0]
		cur.execute(longCountSQL)
		longCount = cur.fetchall()[0][0]		
	except mdb.Error, e:
		sys.exit(1)
	return allCount, prodCount, outageCount, errorCount, _1sCount, _5sCount, longCount

def printFormatedURLMonthlyReport(countlist,url):
	"""the input is allCount, prodCount, outageCount, errorCount, _1sCount, _5sCount, longCount"""
	
	result = "\t\tURL : %s \n" %url
	result += "\t\tproduction status counts \t\t%d\n"	%countlist[1]
	result += "\t\tOutage status counts \t\t\t%d\n"	%countlist[2]
	result += "\t\tError status counts \t\t\t%d\n"	%countlist[3]
	result += "\t\tOther status counts \t\t\t%d\n"	%(countlist[0]-countlist[1]-countlist[2]-countlist[3])
	result += "\t\t=============================================\n"
	result += "\t\tall testing counts \t\t\t%d\n\n"	%countlist[0]
	
	result += "\t\tResponse < 1s counts \t\t\t%d\n"	%countlist[4]
	result += "\t\tResponse between 1,5s counts \t\t%d\n"	%countlist[5]
	result += "\t\tResponse longer than 5s counts \t\t%d\n"	%countlist[6]
	result += "\t\t=============================================\n"
	result += "\t\tall testing counts \t\t\t%d\n\n\n"	%countlist[0]
	
	return result
	
if __name__=='__main__':
	urls = getURLfromdb()
	now = datetime.datetime.now()
	if now.month == 0:
		filename = str(now.year-1) + "-12.html"
	else:
		filename = str(now.year) + "-" + str(now.month-1)+ ".html"
	reportContent = ""
	for url in urls:
		countlist = getURLMonthlyReport(url[0])
		reportContent +=  printFormatedURLMonthlyReport(countlist,url[0])
	conn = boto.connect_s3()
	b = conn.get_bucket('rmsmonthlyreports')
	key = b.new_key(filename)
	key.set_contents_from_string(reportContent)
	key.set_canned_acl('public-read')
	meta = {"Content-Type":"text/plain"}
	key.copy(key.bucket,key.name,preserve_acl=True,metadata=meta)
	#archive the records to archive table
	moveRecords()
