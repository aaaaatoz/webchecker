#create user webchecker and grant privilege 
create user 'webchecker'@'%' identified by '****';
grant all on monitor.* to 'webchecker'@'localhost';

create table DNSchecklog
( timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  hostname varchar(100),
  ip varchar(50),
  status ENUM('production','contingency','other','none'));
  
create table DNSRecords
( hostname varchar(100) not null,
  productionIP varchar(50),
  contingencyIP varchar(50)
  )

 insert into DNSRecords values('www.rms.nsw.gov.au','163.189.7.150','163.189.217.150');
 insert into DNSRecords values('m.rms.nsw.gov.au','163.189.7.150','163.189.217.150');
 insert into DNSRecords values('www.myplates.com.au','163.189.7.166','163.189.217.166');
 insert into DNSRecords values('www.scats.com.au','163.189.7.167','163.189.217.167');
 insert into DNSRecords values('www.sydneymotorways.com.au','163.189.7.162','163.189.217.162');

create table URLRecords (url varchar(200), checked boolean, keywords varchar(20), outagekeyword varchar(20));

create table URLchecklog
( timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  url varchar(200),
  returncode varchar(10),
  status ENUM('production','outage','error','none'));

 insert into URLRecords(url,checked,keywords,outagekeyword) values('http://www.rms.nsw.gov.au',true,'Roads and Maritime Service','outage');
 insert into URLRecords(url,checked,keywords,outagekeyword) values('https://myrta.com/myEToll/',false,'Roads and Maritime Service','outage');
 insert into URLRecords(url,checked,keywords,outagekeyword) values('http://www.myplates.com.au',true,'Roads and Maritime Service','outage');
 insert into URLRecords(url,checked,keywords,outagekeyword) values('http://www.scats.com.au',true,'scats','outage');
 insert into URLRecords(url,checked,keywords,outagekeyword) values('http://sydneymotorways.com',true,'Roads and Maritime Service','outage');
