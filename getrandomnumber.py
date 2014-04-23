#this piece of code is to generate a presedu 'random' by time
import datetime

def getrandomnum():
	now = datetime.datetime.now()
	number = now.year+now.month+now.day+now.hour+now.minute
	return number%1000

if __name__=='__main__':
	print getrandomnum()
