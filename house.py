#!/usr/bin/python
import xml.dom.minidom
from datetime import date, timedelta

#xmltv file
file = "xmltv.xml"

# Show's name, must be spelled exactly the same as it is in the xmltv.xml
showName = "House"

# Day the show airs on. Mon:0, Tues:1 ... Sun:6
airDay = 0

#the channel id
channel = "I78.40949462.microsoft.com"

## Dont change anything below here


doc = xml.dom.minidom.parse(open(file))
rootNode = doc.documentElement

# 0: no upcoming episodes, 1: new, 2: old
rerun = 0

# look at each <programme>
for program in rootNode.getElementsByTagName('programme'):
	# look at the title tag(s)

	for title in program.getElementsByTagName('title'):
		# look at the text of that tag
		for text in title.childNodes:
			# it's the show we want, and we haven't seen any reruns yet
			if text.data == showName and program.attributes['channel'].value == channel and rerun == 0:
				year = int(program.attributes['start'].value[0:4])
				month = int(program.attributes['start'].value[4:6])
				day =  int(program.attributes['start'].value[6:8])
				
				# When ep we're looking at airs
				d = date(year,month,day)
				
				daysAway = d - date.today()
				if d >= date.today() and daysAway < timedelta(days=6) and d.weekday() == airDay:				
					new = program.getElementsByTagName('new')
					if new:
						rerun = 1
					else:
						rerun = 2

print '<html><head><link rel="icon" type="image/png" href="favicon.ico"><title>Is', showName,'A Rerun?</title><body><br><br><br><br><br><center><font size=18 color="FF0000">'
if rerun == 1:
	print "No!"
elif rerun == 2:
	print "Yes"
else:
	print "No House this week :("
print "</font></center></body></html>"
