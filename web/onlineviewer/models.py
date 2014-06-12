from django.db import models

# Create your models here.
class Dnsrecords(models.Model):
    hostname = models.CharField(max_length=100)
    productionip = models.CharField(db_column='productionIP', max_length=50, blank=True) # Field name made lowercase.
    contingencyip = models.CharField(db_column='contingencyIP', max_length=50, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'DNSRecords'

class Dnschecklog(models.Model):
    timestamp = models.DateTimeField()
    hostname = models.CharField(max_length=100, blank=True)
    ip = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=11, blank=True)
    class Meta:
        managed = False
        db_table = 'DNSchecklog'

class Urlrecords(models.Model):
    url = models.CharField(max_length=200, blank=True)
    checked = models.IntegerField(blank=True, null=True)
    keywords = models.CharField(max_length=20, blank=True)
    outagekeyword = models.CharField(max_length=20, blank=True)
    class Meta:
        managed = False
        db_table = 'URLRecords'

class Urlchecklog(models.Model):
    timestamp = models.DateTimeField()
    url = models.CharField(max_length=200, blank=True)
    returncode = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=10, blank=True)
    timeused = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'URLchecklog'

class Urlchecklogarchiver(models.Model):
    timestamp = models.DateTimeField()
    url = models.CharField(max_length=200, blank=True)
    returncode = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=10, blank=True)
    timeused = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'URLchecklogArchiver'

class Proxychecklog(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    proxyname = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=7, blank=True)
    class Meta:
        managed = False
        db_table = 'PROXYchecklog'
