#! /usr/bin/env python
# print('Importing libraries...')
import requests
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree
import sqlite3 as lite



skillDictionary = {}
skillGroups = {}
skills = {}
charSkills = {}


def build_char_skill_list(credentials):
	print('Accessing CharacterSheet API...')
	# payload = {'characterID': characterID, 'keyID': keyID, 'vCode': vCode}
	r = requests.get("http://api.eveonline.com/char/CharacterSheet.xml.aspx", params=credentials)
	charRoot = ET.fromstring(r.text)
	for row in charRoot.find('.//rowset[@name="skills"]'):
		#put skills in charSkills dictionary
		skillID = row.get('typeID')
		level = row.get('level')
		#print('{} {}'.format(skills[typeID], level))
		charSkills[skillID] = [skillDictionary[skillID][1], skillDictionary[skillID][2], skillDictionary[skillID][0], level]
		#print('{} ({}) {} {}'.format(skillDictionary[skillID][1], skillDictionary[skillID][2], skillDictionary[skillID][0], level))
		# charSkills = {skillID: [groupName (0), groupID (1), skillName (2), level (3)] }

def char_wallet_journal(credentials):
	print('Accessing WalletJournal API...')
	r = requests.get("https://api.eveonline.com/char/WalletJournal.xml.aspx", params=credentials)
	charRoot = ET.fromstring(r.text)
	print('\n\nBOUNTIES:')
	for row in charRoot.find('.//rowset[@name="transactions"]'):
		if row.get('refTypeID') == '85' or row.get('refTypeID') == '17':
			print('[{id}] ({date}) | Amount: {amount} | Tax: {tax} | System: {system}'.format(
															id 		= row.get('refID'),
															date	= row.get('date'), 
															amount 	= row.get('amount').rjust(12), 
															tax 	= row.get('taxAmount').rjust(9),
															system 	= row.get('argName1')
														 ))

def corp_wallet_journal(credentials):
	print('Accessing Corp WalletJournal API...')
	r = requests.get("https://api.eveonline.com/corp/WalletJournal.xml.aspx", params=credentials)
	wjRoot = ET.fromstring(r.text)
	print('\n\nWithdrawals')
	for row in wjRoot.find('.//rowset[@name="entries"]'):
		if row.get('refTypeID') == '37':
			print('({date}) | Amount: {amount} | Recipient: {recipient} | Performed by: {agent}'.format(
															date		= row.get('date'),
															amount 		= row.get('amount').rjust(14),
															recipient 	= row.get('ownerName2').ljust(22),
															agent 		= row.get('argName1').ljust(20)
															))


def get_all_trans(credentials):
	print('Pulling all WalletJournal entries...')
	first = None
	r = requests.get("https://api.eveonline.com/corp/WalletJournal.xml.aspx", params=credentials)
	wjRoot = ET.fromstring(r.text)
	count = 0
	for row in wjRoot.find('.//rowset[@name="entries"]'):
		count += 1
		fromID = row.get('refID')

	while count != 0:
		if first is None:
			first = wjRoot
		else:
			first.extend(wjRoot)
		credentials['fromID'] = fromID
		r = requests.get("https://api.eveonline.com/corp/WalletJournal.xml.aspx", params=credentials)
		wjRoot = ET.fromstring(r.text)
		count = 0
		for row in wjRoot.find('.//rowset[@name="entries"]'):
			count += 1
			fromID = row.get('refID')
	return first

	# 	print (ET.tostring(row))



def build_skill_dictionary():
	print('Accessing skills API...')
	skillTree = requests.get("https://api.eveonline.com/eve/SkillTree.xml.aspx")
	skillRoot = ET.fromstring(skillTree.text)
	print('Building skill dictionary...')
	for row in skillRoot.find('.//rowset[@name="skillGroups"]'):
		for skillset in row.find('.//rowset[@name="skills"]'):
			groupID = skillset.get('groupID')
			groupName = row.get('groupName')
			skillID = skillset.get('typeID')
			skillName = skillset.get('typeName')
			if skillID not in skillDictionary:
				skillDictionary[skillID] = [skillName, groupName, groupID]
				#print('SKILL: {} ({}) [{} {}] added.'.format(skillName, skillID, groupName, groupID))

def lookup_group(search_id):
	return skillGroups[search_id]
		
def get_skill_level(skillName):
	return(int(charSkills[skillName]))

def display_char_skills(group=''):
	if group == '':
		print('\nAll skill groups:')
		for l in sorted(charSkills.values()):
			print('[{}] {}: {}'.format(l[0], l[2], l[3]))
	else:
		print('\n\n\'{}\':'.format(group))
		for l in sorted(charSkills.values()):
			if (l[0] == group):
				print('   {}: {}'.format(l[2], l[3]))

def load_char_credentials(filename):
	char = {'characterID': '', 'keyID': '', 'vCode': ''}
	f = open(filename, 'r')
	char['characterID'] = f.readline()
	char['keyID'] = f.readline()
	char['vCode'] = f.readline()
	f.close()
	return char

def load_corp_credentials(filename):
	print('Authenticating for Corp APIs...')
	corp = {'keyID': '', 'vCode': ''}
	f = open(filename, 'r')
	corp['keyID'] = f.readline()
	corp['vCode'] = f.readline()
	f.close()
	return corp


# build_skill_dictionary()
char = load_char_credentials('my_char.txt')
# corp = load_corp_credentials('my_corp.txt')
# build_char_skill_list(char)
# char_wallet_journal(char)
# display_char_skills()
# print(get_skill_level('Retail'))
# corp_wallet_journal(corp)
# print("'walletJournal.xml' updated.")


r = requests.get("https://api.eveonline.com/char/SkillInTraining.xml.aspx", params=char)
root = ET.fromstring(r.text)

print(len(list(root[1])))

# DB_NAME = (r'..\myEVEdb.db')
# conn = lite.connect(DB_NAME)
# curs = conn.cursor()

# query = "select sum(skillpoints) from pilot_skill"
# curs.execute(query)
# for row in curs.fetchall():
# 	print('{:,} total skillpoints'.format(int(row[0])))


# query = "select count(*) from pilot_skill where skillLevel > 0"
# curs.execute(query)
# for row in curs.fetchall():
# 	print('{} total trained skills'.format(int(row[0])))

# query = "select * from key"
# curs.execute(query)
# for row in curs.fetchall():
# 	print(row)
# conn.close()