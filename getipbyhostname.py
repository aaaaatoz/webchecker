import socket
import datetime

def getIPByHostname(host):
	try:
		ip = socket.gethostbyname(host)
	except socket.gaierror:
		ip = ""
	return ip


if __name__=='__main__':
	log = open("/usr/local/webchecker/checklog.log",'a+')
	for line in open(r'/usr/local/webchecker/hostname.conf'):
		if line.strip() =="" or line[0] == '#':
			continue   #pass those are not configuration lines
		checkinfo = line.strip().split()
		currentIP = getIPByHostname (checkinfo[0])
		time = str (datetime.datetime.now())
		if currentIP == checkinfo[1]:
			log.write(time+"\t"+"%s \t\tRunning on Production \t%s\n" %(checkinfo[0],currentIP))
		elif currentIP == checkinfo[2]:
			log.write(time+"\t"+"%s \t\tRunning on Contingency \t%s\n" %(checkinfo[0],currentIP))
		else:
			log.write(time+"\t"+"%s \t\tRunning on \t%s\n" %(checkinfo[0],currentIP))
		log.flush()
	log.close()
		
			
		
