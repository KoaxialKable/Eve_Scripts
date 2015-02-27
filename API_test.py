print('Importing libraries...')
import requests
import xml.etree.cElementTree as ET
from operator import itemgetter

# payload = {'characterID': 94974374, 'userID': 3723024, 'apiKey': '6dTF197MfAXDUadEzcIUD49WcFXEhRSGTht7cV9qBJ38hEa3b7ksgMFZhmHPgbG2'}
# r = requests.get("http://api.eveonline.com/eve/CharacterInfo.xml.aspx", params=payload)
# root = ET.fromstring(r.text)
# result = root.find("result")


#get private character data
# payload = {'characterID': 94974374, 'keyID': 3723024, 'vCode': '6dTF197MfAXDUadEzcIUD49WcFXEhRSGTht7cV9qBJ38hEa3b7ksgMFZhmHPgbG2'}
# r = requests.get("http://api.eveonline.com/char/CharacterSheet.xml.aspx", params=payload)
# charRoot = ET.fromstring(r.text)
print('Accessing skills api...')
skillTree = requests.get("https://api.eveonline.com/eve/SkillTree.xml.aspx")
skillRoot = ET.fromstring(skillTree.text)

skillDictionary = {}
skillGroups = {}
skills = {}
charSkills = {}


def list_char_skills(characterID, keyID, vCode):
	print('Fetching character\'s skills...')
	payload = {'characterID': characterID, 'keyID': keyID, 'vCode': vCode}
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

def display_char_skills():
	print('\nAll skill groups:')
	for l in sorted(charSkills.values()):
		print('[{}] {}: {}'.format(l[0], l[2], l[3]))

def display_char_skills(group):
	print('\n\n\'{}\':'.format(group))
	for l in sorted(charSkills.values()):
		if (l[0] == group):
			print('   {}: {}'.format(l[2], l[3]))

build_skill_dictionary()
list_char_skills('94974374', '3723024', '6dTF197MfAXDUadEzcIUD49WcFXEhRSGTht7cV9qBJ38hEa3b7ksgMFZhmHPgbG2')
display_char_skills('Trade')
# print(get_skill_level('Retail'))

#group skills for printout: alphebetical groups, then within each group, alphabetical skills along with their ranks
