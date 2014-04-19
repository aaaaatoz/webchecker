#create user webchecker and grant privilege 
create user 'webchecker'@'%' identified by '****';
grant all on monitor.* to 'webchecker'@'localhost';
