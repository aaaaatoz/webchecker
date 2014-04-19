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
