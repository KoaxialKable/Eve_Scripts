#! /usr/bin/env python
print('Importing libraries...')
import requests
import xml.etree.cElementTree as ET
# from operator import itemgetter

# payload = {'characterID': 94974374, 'userID': 3723024, 'apiKey': '6dTF197MfAXDUadEzcIUD49WcFXEhRSGTht7cV9qBJ38hEa3b7ksgMFZhmHPgbG2'}
# r = requests.get("http://api.eveonline.com/eve/CharacterInfo.xml.aspx", params=payload)
# root = ET.fromstring(r.text)
# result = root.find("result")


#get private character data
# payload = {'characterID': 94974374, 'keyID': 3723024, 'vCode': '6dTF197MfAXDUadEzcIUD49WcFXEhRSGTht7cV9qBJ38hEa3b7ksgMFZhmHPgbG2'}
# r = requests.get("http://api.eveonline.com/char/CharacterSheet.xml.aspx", params=payload)
# charRoot = ET.fromstring(r.text)
print('Accessing skills API...')
skillTree = requests.get("https://api.eveonline.com/eve/SkillTree.xml.aspx")
skillRoot = ET.fromstring(skillTree.text)

skillDictionary = {}
skillGroups = {}
skills = {}
charSkills = {}
char = {'characterID': '', 'keyID': '', 'vCode': ''}

def build_char_skill_list(payload):
	print('Accessing character API...')
	# payload = {'characterID': characterID, 'keyID': keyID, 'vCode': vCode}
	r = requests.get("http://api.eveonline.com/char/CharacterSheet.xml.aspx", params=payload)
	charRoot = ET.fromstring(r.text)
	for row in charRoot.find('.//rowset[@name="skills"]'):
		#put skills in charSkills dictionary
		skillID = row.get('typeID')
		level = row.get('level')
		#print('{} {}'.format(skills[typeID], level))
		charSkills[skillID] = [skillDictionary[skillID][1], skillDictionary[skillID][2], skillDictionary[skillID][0], level]
		#print('{} ({}) {} {}'.format(skillDictionary[skillID][1], skillDictionary[skillID][2], skillDictionary[skillID][0], level))
		# charSkills = {skillID: [groupName (0), groupID (1), skillName (2), level (3)] }

def build_skill_dictionary():
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

def display_char_skills(group):
	if group == '':
		print('\nAll skill groups:')
		for l in sorted(charSkills.values()):
			print('[{}] {}: {}'.format(l[0], l[2], l[3]))
	else:
		print('\n\n\'{}\':'.format(group))
		for l in sorted(charSkills.values()):
			if (l[0] == group):
				print('   {}: {}'.format(l[2], l[3]))

def load_credentials(filename):
	f = open(filename, 'r')
	char['characterID'] = f.readline()
	char['keyID'] = f.readline()
	char['vCode'] = f.readline()
	f.close()

build_skill_dictionary()
load_credentials('sephrim_rega.txt')
build_char_skill_list(char)
display_char_skills('')
# print(get_skill_level('Retail'))