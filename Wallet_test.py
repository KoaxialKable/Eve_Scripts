#! /usr/bin/env python
print('Importing Libraries...')
import time
import datetime
import requests
import locale
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree
from operator import itemgetter



catagories = []
pilots = {}
db = {}
prize_bounties = {}
current_week = {}
last_week = {}
two_weeks = {}
three_weeks = {}

print('Unpacking Data...')
tree = ET.parse("walletJournal.xml")
root = tree.getroot()

def show_highest_earner():
	print('Calculating overall contribution...')
	count = 0
	for outerRow in root.findall('.//rowset[@name="entries"]'):
		for row in outerRow:
			if row.get('refTypeID') == '85':
				if row.get('ownerName2') not in pilots:
					pilots[row.get('ownerName2')] = float(row.get('amount'))
				else:
					pilots[row.get('ownerName2')] += float(row.get('amount'))
	f = open('highest_earner.txt', 'w')
	for entry in sorted(pilots.items(), key=itemgetter(1), reverse=True):
		f.write('{name}: {amount:.2f}'.format(name=entry[0].ljust(30), amount=float(entry[1])))
		f.write('\n')
		# print ('{name}: {amount:.2f}'.format(name=str(k).ljust(30), amount=v))
	f.close()
	print("  ---'highest_earner.txt' updated.")

def show_weekly_earners():
	print('Calculating per-pilot contribution by week...')
	for outerRow in root.findall('.//rowset[@name="entries"]'):
		for row in outerRow:
			refTypeID = row.get('refTypeID')
			if refTypeID == '85':
				# Prize Bounties
				name = row.get('ownerName2')
				amount = float(row.get('amount'))
				# date = row.get('date')
				date = time.strptime(row.get('date'), "%Y-%m-%d %H:%M:%S")
				date = datetime.datetime(*date[:6])
				if name not in prize_bounties:
					prize_bounties[name] = [{'amount': amount, 'date': date}]
				else:
					prize_bounties[name].append({'amount': amount, 'date': date})
	#past 7 days
	for row in prize_bounties:
		for record in prize_bounties[row]:
			# days old
			# date = datetime.fromtimestamp(mktime(record['date']))
			# date = datetime.datetime(*record['date'][:6])
			delta = datetime.datetime.now() - record['date']
			amount = record['amount']
			if (delta.days < 7):
				#this week
				if row not in current_week:
					current_week[row] = amount
				else:
					current_week[row] += amount
			elif (7 < delta.days and delta.days < 14):
				# last week
				if row not in last_week:
					last_week[row] = amount
				else:
					last_week[row] += amount
			elif (14 < delta.days and delta.days < 21):
				if row not in two_weeks:
					two_weeks[row] = amount
				else:
					two_weeks[row] += amount
			elif (21 < delta.days and delta.days < 28):
				if row not in three_weeks:
					three_weeks[row] = amount
				else:
					three_weeks[row] += amount
	print('Generating report...')

	f = open('weekly_breakdown.txt', 'w')
	count = 1
	print('This week', file=f)
	for row in sorted(current_week.items(), key=itemgetter(1), reverse=True):
		print('\t{rank} {name} : {amount:,.2f}'.format(rank=str(count).ljust(3), name=row[0].rjust(29), amount=row[1]), file=f)
		count += 1

	count = 1
	print('\n\nLast Week', file=f)
	for row in sorted(last_week.items(), key=itemgetter(1), reverse=True):
		print('\t{rank} {name} : {amount:,.2f}'.format(rank=str(count).ljust(3), name=row[0].rjust(29), amount=row[1]), file=f)
		count += 1

	count = 1
	print('\n\nTwo Weeks Ago', file=f)
	for row in sorted(two_weeks.items(), key=itemgetter(1), reverse=True):
		print('\t{rank} {name} : {amount:,.2f}'.format(rank=str(count).ljust(3), name=row[0].rjust(29), amount=row[1]), file=f)
		count += 1

	count = 1
	print('\n\nThree Weeks Ago', file=f)
	for row in sorted(three_weeks.items(), key=itemgetter(1), reverse=True):
		print('\t{rank} {name} : {amount:,.2f}'.format(rank=str(count).ljust(3), name=row[0].rjust(29), amount=row[1]), file=f)
		count += 1
	f.close()
	print('"weekly_breakdown.txt" updated.')

# show_highest_earner()
show_weekly_earners()