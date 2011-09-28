#!/home7/opennot1/bin/python

# get_TLE.py copyright (C) 2011 Nathan Bergey <nathan.bergey@gmail.com>
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

# This should get a recent TLE direct from the source - NASA's tracking 
# department 

import urllib2
import datetime

# NASA's station FDO updates this page with very precise data. Only using a 
# small bit of it for now.

url = "http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html"

# Open a http request
req = urllib2.Request(url)
response = urllib2.urlopen(req)
data = response.read()

# parse the HTML BOOO SCRAPING >:o
data = data.split("<PRE>")[1]
data = data.split("</PRE>")[0]
data = data.split("Vector Time (GMT): ")[1:]

for group in data:
  # Time the vector is valid for
  dt = group[0:17]
  dt = datetime.datetime.strptime(dt, "%Y/%j/%H:%M:%S")
  
  tle = group.split("TWO LINE MEAN ELEMENT SET")[1]
  tle = tle[8:160]
  lines = tle.split('\n')[0:3]
  
  # Most recent TLE
  now = datetime.datetime.utcnow()
  if (dt - now).days >= 0: 
    
    # Debug Printing
    """
    print dt
    for line in lines:
      print line.strip()
    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    """
    
    # Write to file
    f_out = open('iss.tle','w')
    for line in lines:
      f_out.write(line.strip() + "\n")
    
    # Done.
    f_out.close()
    break
    
