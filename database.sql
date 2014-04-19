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
