import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'webchecker', '', 'monitor');
    cur = con.cursor()
    cur.execute("select * from DNSRecords")
    records = cur.fetchall()
    for record in records:
        print record
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:    
    if con:    
        con.close()
