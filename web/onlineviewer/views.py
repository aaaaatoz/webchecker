from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
#import models
from onlineviewer.models import Dnsrecords
from onlineviewer.models import Dnschecklog
from onlineviewer.models import Urlrecords
from onlineviewer.models import Urlchecklog
from onlineviewer.models import Urlchecklogarchiver
from onlineviewer.models import Proxychecklog 

from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.core.paginator import Paginator
import datetime 
from datetime import time

#define a helper function to get the midnight time
def getmidnight(dt):
    min_pub_date_time = datetime.datetime.combine(dt.date(), time.min)
    max_pub_date_time = datetime.datetime.combine(dt.date(), time.max)
    return min_pub_date_time,max_pub_date_time



# Create your views here.
@login_required
def viewurltests(request):
    day = request.GET.get('day', '')
    checkingurl = request.GET.get('url', 'all')
    selectstatus = request.GET.get('status', 'all')
    if day == '':	#no date is passing, using top 20
        checkingday = datetime.datetime.now()
    else:	#parse the day and time
        #the web server will pass a date as '2014-05-08';
       checkingday = datetime.datetime.strptime(day, '%Y-%m-%d')
    starttime,endtime = getmidnight(checkingday)

    url= Urlchecklog.objects.all().filter(timestamp__gte=starttime, timestamp__lte=endtime)
    if len(url) == 0:
        url= Urlchecklogarchiver.objects.all().filter(timestamp__gte=starttime, timestamp__lte=endtime)   
    if selectstatus <> 'all':
        url = url.filter(status = selectstatus)

    if checkingurl <> 'all':
        url = url.filter(url= checkingurl)
    url = url.order_by('-timestamp')
    #url= Urlchecklog.objects.all().filter(status=selectstatus).filter(timestamp__gte=starttime, timestamp__lte=endtime).order_by('-timestamp')
    return render_to_response ("URL.html",{"user":request.user,"URLresults":url},
                               context_instance = RequestContext(request))
@login_required
def viewdnstests(request):
    day = request.GET.get('day', '')
    checkingdns = request.GET.get('dns', 'all')
    selectstatus = request.GET.get('status', 'all')
    if day == '':	#no date is passing, using top 20
        checkingday = datetime.datetime.now()
    else:	#parse the day and time
        #the web server will pass a date as '2014-05-08';
       checkingday = datetime.datetime.strptime(day, '%Y-%m-%d')
    starttime,endtime = getmidnight(checkingday)

    dns = Dnschecklog.objects.all().filter(timestamp__gte=starttime, timestamp__lte=endtime)
    if selectstatus <> 'all':
        dns = dns.filter(status = selectstatus)

    if checkingdns <> 'all':
        dns  = dns.filter(hostname = checkingdns)
    dns = dns.order_by('-timestamp')
    return render_to_response ("DNS.html",{"user":request.user,"DNSresults":dns},
                               context_instance = RequestContext(request))

@login_required
def viewproxystatus(request):
    day = request.GET.get('day', '')
    checkingproxy = request.GET.get('proxy', 'all')
    selectstatus = request.GET.get('status', 'all')
    if day == '':	#no date is passing, using top 20
        checkingday = datetime.datetime.now()
    else:	#parse the day and time
        #the web server will pass a date as '2014-05-08';
       checkingday = datetime.datetime.strptime(day, '%Y-%m-%d')
    starttime,endtime = getmidnight(checkingday)

    proxy = Proxychecklog.objects.all().filter(timestamp__gte=starttime, timestamp__lte=endtime)
    if selectstatus <> 'all':
        proxy = proxy.filter(status = selectstatus)

    if checkingproxy <> 'all':
        proxy  = proxy.filter(proxyname = checkingproxy )
    proxy = proxy.order_by('-timestamp')
    return render_to_response ("PROXY.html",{"user":request.user,"PROXYresults":proxy},
                               context_instance = RequestContext(request))
