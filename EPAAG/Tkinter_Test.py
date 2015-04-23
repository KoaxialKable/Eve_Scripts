#! /usr/bin/env python
from tkinter import *
import requests
import xml.etree.cElementTree as ET
import sqlite3 as lite
import os

DB_NAME = 'myEVEdb.db'
conn = lite.connect(DB_NAME)
curs = conn.cursor()

# create 'pilot' table it not exists
curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pilot'")
if curs.fetchone() is None:
	curs.execute(
				'''
				create table pilot(
					characterID 		text primary key
					,name 				text
					,homeStationID 		text
					,corpID 			text
					,corpName 			text
					,allianceID 		text
					,allianceName 		text
					,intelligence 		text
					,memory 			text
					,charisma 			text
					,perception 		text
					,willpower 			text
					,skillInTrainingID 	text
					,trainingEndTime 	text
					,trainingToLevel 	text
					,walletBalance 		real
				)
				'''
	)


curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skill'")
if curs.fetchone() is None:
	curs.execute(
				'''
				create table skill(
					skillID 			text primary key
					,name 				text
					,rank 				real
					,groupID 			text
					,primaryAttribute 	text
					,secondaryAttribute text
					,published 			text
				)
				'''
	)

curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skillReq'")
if curs.fetchone() is None:
	curs.execute(
				'''
				create table skillReq(
					skillID 			text
					,requiredSkillID 	text
					,requiredLevel 		real
				)
				'''
	)

curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pilot_skill'")
if curs.fetchone() is None:
	curs.execute(
				'''
				create table pilot_skill(
					characterID 		text
					,skillID 			text
					,skillLevel 		real
					,skillPoints 		real
				)
				'''
	)

conn.commit()
conn.close()

def checkDB(table, attribute, value):
	conn = lite.connect(DB_NAME)
	curs = conn.cursor()

	param = (value,)
	query = "SELECT name FROM " + table + " WHERE " + attribute + " = ?"
	curs.execute(query, param)
	if curs.fetchone() is None:
		conn.close()
		return False
	conn.close()
	return True

def fetchPilotData(charName):
	""" Get pilot data from DB only """
	print('DB polled for {}'.format(charName))

	conn = lite.connect(DB_NAME)
	curs = conn.cursor()
	param = (charName,)
	query =  "SELECT characterID, name, homeStationID, corpID, corpName, allianceID, allianceName, intelligence, "
	query += "memory, charisma, perception, willpower, skillInTrainingID, trainingEndTime, trainingToLevel, walletBalance "
	query += "from pilot where name = ?"

	curs.execute(query, param)
	result = curs.fetchone()

	pilot = {
		'characterID': ''
		,'name': ''
		,'homeStationID': ''
		,'corpID': ''
		,'corpName': ''
		,'allianceID': ''
		,'allianceName': ''
		,'intelligence': ''
		,'memory': ''
		,'charisma': ''
		,'perception': ''
		,'willpower': ''
		,'skillInTrainingID': ''
		,'trainingEndTime': ''
		,'trainingToLevel': ''
		,'walletBalance': 0 
	}


	pilot['characterID'] = result[0]
	pilot['name'] = result[1]
	pilot['homeStationID'] = result[2]
	pilot['corpID'] = result[3]
	pilot['corpName'] = result[4]
	pilot['allianceID'] = result[5]
	pilot['allianceName'] = result[6]
	pilot['intelligence'] = result[7]
	pilot['memory'] = result[8]
	pilot['charisma'] = result[9]
	pilot['perception'] = result[10]
	pilot['willpower'] = result[11]
	pilot['skillInTrainingID'] = result[12]
	pilot['trainingEndTime'] = result[13]
	pilot['trainingToLevel'] = result[14]
	pilot['walletBalance'] = float(result[15])

	conn.close()
	return pilot

def get_all_keyfiles(directory):
	files = []
	for filename in os.listdir(directory):
		if filename.endswith(".txt"):
			files.append(filename)
	return files


class Application(Frame):
	""" A GUI application """
 
	def __init__(self, master):
		""" Initialize the Frame """
		Frame.__init__(self, master)
		self.grid()
		self.load_chars()
		self.roster = self.roll_call()
		self.create_widgets()
 
	def create_widgets(self):
		""" Create stuff """
		#create one button
		self.button1 = Button(self, text="Load Selected Pilot", command=self.loadPilot, width=15)
		self.button1.grid(row=0, column=1, columnspan=2, sticky=W)

		self.p_characterID = Label(self, text="Character ID: ")
		self.p_characterID.grid(row=1, column=0, sticky=W)

		self.p_name = Label(self, text="Name: ")
		self.p_name.grid(row=2, column=0, sticky=W)

		self.p_homeStationID = Label(self, text="Home Station: ")
		self.p_homeStationID.grid(row=3, column=0, sticky=W)

		self.p_corpName = Label(self, text="Corp Name: ")
		self.p_corpName.grid(row=4, column=0, sticky=W)

		self.p_allianceName = Label(self, text="AllianceName: ")
		self.p_allianceName.grid(row=5, column=0, sticky=W)

		self.p_intelligence = Label(self, text="Intelligence: ")
		self.p_intelligence.grid(row=6, column=0, sticky=W)

		self.p_memory = Label(self, text="Memory: ")
		self.p_memory.grid(row=7, column=0, sticky=W)

		self.p_charisma = Label(self, text="Charisma: ")
		self.p_charisma.grid(row=8, column=0, sticky=W)

		self.p_perception = Label(self, text="Perception: ")
		self.p_perception.grid(row=9, column=0, sticky=W)

		self.p_willpower = Label(self, text="Willpower: ")
		self.p_willpower.grid(row=10, column=0, sticky=W)

		self.p_skillInTrainingID = Label(self, text="Currently Training: ")
		self.p_skillInTrainingID.grid(row=11, column=0, sticky=W)

		self.p_trainingEndTime = Label(self, text="Training End Time: ")
		self.p_trainingEndTime.grid(row=12, column=0, sticky=W)

		self.p_trainingToLevel = Label(self, text="Training To Level: ")
		self.p_trainingToLevel.grid(row=13, column=0, sticky=W)

		self.p_walletBalance = Label(self, text="Wallet Balance: ")
		self.p_walletBalance.grid(row=14, column=0, sticky=W)



		self.selectedPilot = StringVar()
		self.selectedPilot.set(self.roster[0])
		self.rosterMenu = OptionMenu(self, self.selectedPilot, *self.roster)
		self.rosterMenu.grid(row=0, column=0, sticky=W)
 
	def loadPilot(self):
		name = self.selectedPilot.get()
		if name == "no pilots":
			return
		pilot = fetchPilotData(name)

		# set all widgets to pilot's data
		self.p_characterID["text"] = "Character ID: {}".format(pilot['characterID'])
		self.p_name["text"] = "Name: {}".format(pilot['name'])
		self.p_homeStationID["text"] = "Home Station: {}".format(pilot['homeStationID'])
		self.p_corpName["text"] = "Corp Name: {}".format(pilot['corpName'])
		self.p_allianceName["text"] = "AllianceName: {}".format(pilot['allianceName'])
		self.p_intelligence["text"] = "Intelligence: {}".format(pilot['intelligence'])
		self.p_memory["text"] = "Memory: {}".format(pilot['memory'])
		self.p_charisma["text"] = "Charisma: {}".format(pilot['charisma'])
		self.p_perception["text"] = "Perception: {}".format(pilot['perception'])
		self.p_willpower["text"] = "Willpower: {}".format(pilot['willpower'])
		self.p_skillInTrainingID["text"] = "Currently Training: {}".format(pilot['skillInTrainingID'])
		self.p_trainingEndTime["text"] = "Training End Time: {}".format(pilot['trainingEndTime'])
		self.p_trainingToLevel["text"] = "Training To Level: {}".format(pilot['trainingToLevel'])
		self.p_walletBalance["text"] = "Wallet Balance: {:,.2f}".format(pilot['walletBalance'])

	def roll_call(self):
		""" Find the names of all known pilots and populate the OptionMenu """
		roster = []
		conn = lite.connect(DB_NAME)
		curs = conn.cursor()
		curs.execute("select name from pilot")
		result = curs.fetchall()
		if not result == []:
			for pilot in result:
				roster.append(pilot[0])
		else:
			roster.append("no pilots")
		return roster

	# def refreshOptionMenu(self):
	# 	self.roster = []
	# 	self.roster = self.roll_call()
	# 	self.selectedPilot.set(self.roster[0])
	# 	self.rosterMenu = None
	# 	self.rosterMenu = OptionMenu(self, self.selectedPilot, *self.roster)
	# 	self.rosterMenu.grid(row=0, column=0, sticky=W)

	def load_chars(self):
		""" Go through all the keyfiles and populate API data for all characters """
		conn = lite.connect(DB_NAME)
		curs = conn.cursor()

		# create a list of all keyfiles available
		charKeys = get_all_keyfiles("chars")

		# access each API, get data, put in DB
		for charKey in charKeys:
			print('charKey = {}'.format(charKey))

			char = {
				'characterID': ''
				,'keyID': ''
				,'vCode': ''
			}
			
			filename = '.\\chars\\' + charKey

			f = open(filename, 'r')
			char['characterID'] = f.readline().rstrip('\n')
			char['keyID'] = f.readline().rstrip('\n')
			char['vCode'] = f.readline().rstrip('\n')
			f.close()

			pilot = {
				'characterID': ''
				,'name': ''
				,'homeStationID': ''
				,'corpID': ''
				,'corpName': ''
				,'allianceID': ''
				,'allianceName': ''
				,'intelligence': ''
				,'memory': ''
				,'charisma': ''
				,'perception': ''
				,'willpower': ''
				,'skillInTrainingID': ''
				,'trainingEndTime': ''
				,'trainingToLevel': ''
				,'walletBalance': 0 
			}

			pilot_skills = []

			# check if character already in DB file and clean old data
			exists = checkDB('pilot', 'characterID', char['characterID'])
			print('Check on pilot returned {}'.format(exists))
			if exists:
				print('Purging old data for {}'.format(char['characterID']))
				curs.execute("delete from pilot where characterID = ?", (char['characterID'],))
				curs.execute("delete from pilot_skill where characterID = ?", (pilot['characterID'],))
				conn.commit()

			r = requests.get("https://api.eveonline.com/char/CharacterSheet.xml.aspx", params=char)
			root = ET.fromstring(r.text)

			pilot['characterID'] = root[1][0].text
			pilot['name'] = root[1][1].text
			pilot['homeStationID'] = root[1][2].text
			pilot['corpID'] = root[1][9].text
			pilot['corpName'] = root[1][8].text
			pilot['allianceID'] = root[1][11].text
			pilot['allianceName'] = root[1][10].text
			pilot['intelligence'] = root[1][30][0].text
			pilot['memory'] = root[1][30][1].text
			pilot['charisma'] = root[1][30][2].text
			pilot['perception'] = root[1][30][3].text
			pilot['willpower'] = root[1][30][4].text
			pilot['walletBalance'] = float(root[1][28].text)

			for row in root.find('.//rowset[@name="skills"]'):
				skill_entry = (
					pilot['characterID']
					,row.get('typeID')
					,row.get('level')
					,row.get('skillpoints')
				)

				pilot_skills.append(skill_entry)

			r = requests.get("https://api.eveonline.com/char/SkillInTraining.xml.aspx", params=char)
			root = ET.fromstring(r.text)

			if len(list(root[1])) == 8:
				pilot['skillInTrainingID'] = root[1][3].text
				pilot['trainingEndTime'] = root[1][1].text
				pilot['trainingToLevel'] = root[1][6].text
			else:
				pilot['skillInTrainingID'] = 'Not training'
				pilot['trainingEndTime'] = 'n/a'
				pilot['trainingToLevel'] = 'n/a'



			print('API polled for {}'.format(pilot['name']))
			param = (
				pilot['characterID']
				,pilot['name'] 
				,pilot['homeStationID']
				,pilot['corpID']
				,pilot['corpName']
				,pilot['allianceID']
				,pilot['allianceName']
				,pilot['intelligence']
				,pilot['memory']
				,pilot['charisma']
				,pilot['perception']
				,pilot['willpower']
				,pilot['skillInTrainingID']
				,pilot['trainingEndTime']
				,pilot['trainingToLevel']
				,pilot['walletBalance']
			)
			# insert pilot data into DB
			command =  "insert into pilot (characterID, name, homeStationID, corpID, corpName, allianceID, allianceName, intelligence, "
			command += "memory, charisma, perception, willpower, skillInTrainingID, trainingEndTime, trainingToLevel, walletBalance) "
			command += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
			curs.execute(command, param)
			conn.commit()

			#insert pilot_skill data into DB
			curs.executemany("insert into pilot_skill (characterID, skillID, skillLevel, skillPoints) VALUES (?, ?, ?, ?)", pilot_skills)
			conn.commit()
			print('Database updated correctly for {}\n'.format(pilot['name']))

		print('All character keyfiles accounted for.\n')
		conn.close()



# Program starts here
root = Tk()

root.title("EVE Online Pilot At-A-Glance")
root.geometry("600x800")
 
app = Application(root)
 
root.mainloop()