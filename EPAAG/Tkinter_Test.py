#! /usr/bin/env python
from tkinter import *
import requests
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree
import sqlite3 as lite

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
				);
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
	# authenticate for API, from external file
	char = {
		'characterID': ''
		,'keyID': ''
		,'vCode': ''
	}
	
	filename = '.\\chars\\' + charName + '.txt'

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

	# check if character already in DB file
	exists = checkDB('pilot', 'characterID', char['characterID'])
	print('Check on pilot returned {}'.format(exists))
	conn = lite.connect(DB_NAME)
	curs = conn.cursor()


	if not exists:
		# if new character, poll API for data
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

		pilot['skillInTrainingID'] = root[1][3].text
		pilot['trainingEndTime'] = root[1][1].text
		pilot['trainingToLevel'] = root[1][6].text



		print('API polled')
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

		#insert pilot_skill data into DB
		curs.execute("delete from pilot_skill where characterID = ?", (pilot['characterID'],))
		curs.executemany("insert into pilot_skill (characterID, skillID, skillLevel, skillPoints) VALUES (?, ?, ?, ?)", pilot_skills)
		conn.commit()
	else:
		# if existing character, poll DB for data
		print('DB polled')
		param = (char['characterID'],)
		curs.execute("SELECT name FROM pilot WHERE characterID = ?", param)
		result = curs.fetchone()
		pilot['name'] = result[0]

	conn.close()
	return pilot




class Application(Frame):
	""" A GUI application """
 
	def __init__(self, master):
		""" Initialize the Frame """
		Frame.__init__(self, master)
		self.grid()
		self.roster = self.roll_call()
		self.create_widgets()
 
	def create_widgets(self):
		""" Create stuff """
		#create one button
		self.button1 = Button(self, text="Update Pilot's Info", command=self.updatePilot, width=15)
		self.button1.grid(row=0, column=1, columnspan=2, sticky=W)

		self.label = Label(self, text="Pilot's name is: ")
		self.label.grid(row=1, column=0, sticky=W)


		self.selectedPilot = StringVar()
		self.selectedPilot.set(self.roster[0])
		self.rosterMenu = OptionMenu(self, self.selectedPilot, *self.roster)
		self.rosterMenu.grid(row=0, column=0, sticky=W)
 
	def updatePilot(self):
		name = self.selectedPilot.get()
		print('name to be looked up: {}'.format(name))
		if name == "no pilots":
			pilot = fetchPilotData("new_char")
		else:
			pilot = fetchPilotData(name)
		self.label["text"] = "Pilot's name is: {}".format(pilot['name'])
		self.refreshOptionMenu()

	def roll_call(self):
		""" Find the names and IDs of all known pilots """
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

	def refreshOptionMenu(self):
		self.roster = []
		self.roster = self.roll_call()
		self.selectedPilot.set(self.roster[0])
		self.rosterMenu = None
		self.rosterMenu = OptionMenu(self, self.selectedPilot, *self.roster)
		self.rosterMenu.grid(row=0, column=0, sticky=W)




# Program starts here
root = Tk()

root.title("EVE Online Pilot At-A-Glance")
root.geometry("600x800")
 
app = Application(root)
 
root.mainloop()