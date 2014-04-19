import dns.resolver

r = dns.resolver.Resolver() 
r.namerservers =  [r'dns1.rta.nsw.gov.au'] 
# or any other IP, in my case I'm using PDNS, which have two 
# parts: a recursor and a resolver; recursor allows requests only 
# on localhost 

record = r.query("rta.nsw.gov.au", 'A').response 
print record
