#!/home7/opennot1/bin/python

# ISS pass prediction copyright (C) 2011 Nathan Bergey <nathan.bergey@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
# 
# Full licence is in the file COPYING and at http://www.gnu.org/copyleft/gpl.html

import cgi
import cgitb
#cgitb.enable() #for testing
import os, site, sys; 
site.addsitedir(os.path.expanduser('~/lib/python2.4/site-packages/simplejson-2.1.6-py2.4-linux-x86_64.egg'))
site.addsitedir(os.path.expanduser('~/lib/python2.4/site-packages/pyephem-3.7.4.1-py2.4-linux-x86_64.egg'))


def giveup():
  """Catch some kind of major failure and return the message 'failure'"""
  print "Content-Type: application/json;charset=utf-8"
  print
  print '{message: "failure"}'
  sys.exit("catch")

# Try to import some non-standard packages
try:
  import ephem
  import simplejson
  import datetime
  import time
except:
  giveup()

# Read the magic TLE from the file system. This is expected to be updated by someone else
try:
  tle_file = open("iss.tle", 'r')
except:
  giveup()
  
tle = []
data = tle_file.read()
tle = data.split('\n')

# Catch a bad TLE file
if len(tle) < 3:
  giveup()

# API defaults
latitude    = '0.0'  # String of lat in decimal degrees
longitude   = '0.0'  # String of lon in decimal degrees
altitude    = 0      # int altitude MSL [meters]
num_passes  = 1      # int number of passes to predict

# get data from query string
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
    altitude = int(post_data["alt"].value)
  except:
    pass

if "n" in post_data.keys():
  try:
    num_passes = int(post_data["n"].value)
  except:
    pass

# Sanitize num_pass
if num_passes <= 0: num_passes = 1
if num_passes > 100: num_passes = 100

# Space Station parameters
iss = ephem.readtle(tle[0], tle[1], tle[2])

# Set location
location = ephem.Observer()
location.lat        = str(latitude)
location.long       = str(longitude)
location.elevation  = altitude

# Override refration calculation
location.pressure   = 0
location.horizon    = '5:00'

# Set time now
now                 = datetime.datetime.utcnow()
location.date       = now

# List of passes
passes = []

# Make predictions
for p in range(num_passes):
	tr, azr, tt, altt, ts, azs = location.next_pass(iss)
	duration = int((ts - tr) *60*60*24)
	year, month, day, hour, minute, second = tr.tuple()
	dt = datetime.datetime(year, month, day, hour, minute, int(second))
	
	passes.append({"risetime": int(time.mktime(dt.timetuple())), "duration": duration})
	
	# Increase the time by more than a pass and less than an orbit
	location.date = tr + 25*ephem.minute

# Return object
obj = {"request": {  "datetime":  int(time.mktime(now.timetuple()))
                    ,"latitude":  latitude
                    ,"longitude": longitude
                    ,"altitude":  altitude
                    ,"passes":    num_passes}
       ,"response": passes
       ,"message": "success"}

# print data
print "Content-Type: application/json;charset=utf-8"
print

print simplejson.dumps(obj)
