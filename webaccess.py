import datetime
import urllib2
import time
import shutil

def accessweb(proxyname):
        result = False
        try:
                conn = ""
                proxy = urllib2.ProxyHandler({'http': 'http://****:*****@'+proxyname+':8888'})
                auth = urllib2.HTTPBasicAuthHandler()
                opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                url = "http://54.206.61.137/%s" %proxyname
                conn = urllib2.urlopen(url,timeout=5)
                httpCode = conn.getcode()
                if httpCode == 200:
                        response = conn.read()
                        result = True
        except Exception,e:
                result = False
        finally:
                if conn:
                        conn.close()
                return result

if __name__=='__main__':
        shutil.move('proxy.cfg','proxy.cfg'+"~")
        dest = open('proxy.cfg',"w")
        source = open('proxy.cfg'+"~","r")
        for line in source:
                proxy, counter = line.strip().split()
                if int (counter) < 9 :
                        dest.write(proxy+"\t"+ str( int(counter)+1)+"\n")
                else:
                        result = accessweb(proxy)
                        if result:
                                dest.write(proxy+"\t"+"0\n")
                        else:
                                dest.write(proxy+"\t"+ str( int(counter)+1)+"\n")
                dest.flush()
        dest.close()
        source.close()

