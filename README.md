## Eve_Scripts
Some Eve_API scripts I've been tinkering with.

#### API TESTS
This is just where I first started employing python to interface with Eve Online's api.

#### EPAAG (Eve Pilots at-a-Glance)
*Under heavy construction!*
A tool using the Tkinter library to generate a windowed application written in python.
I can't really compete with other apps or services out there, so I guess we'll just see where it ends up.

**Important**
If you choose to clone this and use it to see what it does, you will need to do a few things.
* EPAAG loads character API key data from `.txt` files located in the `chars` folder. It will just look inside its own directory for that folder.
* The API information should take the following form:
(I choose to name the txt files after the character they belong to, for simplicity)
Filename: `CharacterName.txt`
The contents of the file will be:
* CharacterID
* KeyID
* Verification Code

So a file would look like this:
```
24678957
5612378
7cV9qBJ38hEa3b7ksgMFZhmHPgbG26dTF197MfAXDUadEzcIUD49WcFXEhRSGTht
```

If you've done it correctly, running `Tkinter_Test.py` should load the most basic (probably uninteresting) information about your character!

Check back now and then for updates.
