#!/home7/opennot1/bin/python

# ISS location copyright (C) 2011 Nathan Bergey <nathan.bergey@gmail.com>
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
import math
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

origin = datetime.datetime(1970, 1, 1, 0, 0, 0)

def unixtime(dt):
  global origin
  delta = (dt - origin)
  seconds = delta.seconds
  days = delta.days
  return days*86400 + seconds

 
# Read the magic TLE from the file system. This is expected to be updated by someone else
try:
  tle_file = open("../iss/iss.tle", 'r')
except:
  giveup()

now = datetime.datetime.utcnow()

tle = []
data = tle_file.read()
tle = data.split('\n')

# Catch a bad TLE file
if len(tle) < 3:
  giveup()

iss = ephem.readtle(tle[0], tle[1], tle[2])
iss.compute(now)

lon = math.degrees(iss.sublong)
lat = math.degrees(iss.sublat)

obj = {'message': 'success', 'timestamp': unixtime(now), 'iss_position': {'latitude': lat, 'longitude':lon} }

# print data
print "Content-Type: application/json;charset=utf-8"
print

print simplejson.dumps(obj)
