#! /usr/bin/env python
print('Importing Libraries...')
import requests
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree
from operator import itemgetter

catagories = []
pilots = {}

print('Unpacking Data...')
tree = ET.parse("xmldump2.xml")
root = tree.getroot()

def show_highest_earner():
	count = 0
	for outerRow in root.findall('.//rowset[@name="entries"]'):
		for row in outerRow:
			if row.get('refTypeID') == '85':
				if row.get('ownerName2') not in pilots:
					pilots[row.get('ownerName2')] = float(row.get('amount'))
				else:
					pilots[row.get('ownerName2')] += float(row.get('amount'))
	f = open('report.txt', 'w')
	for entry in sorted(pilots.items(), key=itemgetter(1), reverse=True):
		f.write('{name}: {amount:.2f}'.format(name=entry[0].ljust(30), amount=float(entry[1])))
		f.write('\n')
		# print ('{name}: {amount:.2f}'.format(name=str(k).ljust(30), amount=v))
	f.close()

show_highest_earner()