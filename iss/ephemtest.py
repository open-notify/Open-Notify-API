#!/home7/opennot1/bin/python
import cgi
import cgitb
cgitb.enable()
import os, site, sys; 
site.addsitedir(os.path.expanduser('~/lib/python2.4/site-packages/simplejson-2.1.6-py2.4-linux-x86_64.egg'))
site.addsitedir(os.path.expanduser('~/lib/python2.4/site-packages/pyephem-3.7.4.1-py2.4-linux-x86_64.egg'))

def giveup():
  print "Content-Type: application/json;charset=utf-8"
  print
  print '{message: "failure"}'
  sys.exit("catch")

try:
  import ephem
  import simplejson
  import datetime
except:
  giveup()

try:
  tle_file = open("iss.tle", 'r')
except:
  giveup()
  
tle = []
data = tle_file.read()
tle = data.split('\n')

if len(tle) < 3:
  giveup()

# Space Station
iss = ephem.readtle(tle[0], tle[1], tle[2])

# location defaults
latitude  = '0.0'
longitude = '0.0'
altidue   = 0
n         = 1

# get location from query string
post_data = cgi.FieldStorage()

if "lat" in post_data.keys():
  try:
    latitude = float(post_data["lat"].value)
  except:
    pass

if "lon" in post_data.keys():
  try:
    longitude = float(post_data["lon"].value)
  except:
    pass

if "alt" in post_data.keys():
  try:
    altidue = int(post_data["alt"].value)
  except:
    pass

if "n" in post_data.keys():
  try:
    n = int(post_data["n"].value)
  except:
    pass
    
if n <= 0:
  n = 1

if n > 100:
  n = 100
    
# Set location
location = ephem.Observer()
location.lat        = str(latitude)
location.long       = str(longitude)
location.elevation  = altidue

# Override refration calculation
location.pressure   = 0
location.horizon    = '5:00'

# Set time now
location.date       = datetime.datetime.utcnow()

# List of passes
passes = []

for p in range(n):
	tr, azr, tt, altt, ts, azs = location.next_pass(iss)
	duration = int((ts - tr) *60*60*24)
	year, month, day, hour, minute, second = tr.tuple()
	dt = datetime.datetime(year, month, day, hour, minute, int(second))
	passes.append({"rise-time": dt.isoformat(), "duration": duration})
	location.date = tr + 20*ephem.minute

# print data
print "Content-Type: application/json;charset=utf-8"
print

print simplejson.dumps(passes)
