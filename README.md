![Austeritas Logo](https://github.com/AXOMEstudios/austeritas/raw/master/Austeritas%20with%20Text.png)

# Austeritas
Austeritas is an amazingly easy-to-use server moderation system for Bedrock Dedicated Servers (BDS) which allows you to remotely keep track of your moderation tasks by simply using the Austeritas online interface.

---

## Installation
### Requirements
Austeritas requires your bedrock server to run inside a screen session because it needs to communicate with the session over the terminal.
As well, Austeritas requires you to install the pip depedencies listed in requirements.txt.

### How to get started
Before you start Austeritas the very first time, please run install.py to create the essential files for the app.
You should edit the constants.py file then. Set ALLOW_NEW_USERS to True. Then start the server and access it via the web browser of your choice.
Click on "Log in", then enter your wished credentials in the section "Generate new user". Copy the JSON you get and paste it into the array "users" in the file austeritas_config.json, set ALLOW_NEW_USERS to False inside of constants.py and restart the server.
You are now able to log in using these credentials.

---

## Features

### Kicking
Easily kick players from the web interface. Warn them, save their names to a list for quick access - and all of that without even joining the server!

### Banning
You can ban persons over a specific amount of time using a comprehensible User Interface - without commands, add-ons or plug-ins at all! Your world can be kept entirely vanilla while still maintaining a great moderation performance.

### Warnings
Warn players by the click of a button! Austeritas remembers the warnings for each player and provides tools for automatic action to be taken upon a player reaches a specific level of warnings.

### Accessible from everywhere, anytime!
Austeritas can be used from wherever you are - your personal moderation assistant is right at your fingertips, gaining you the ability of reacting immediately once something suspicious happens.

### Lightweight
Austeritas doesn't make your server lag badly - by using sophisticated, performance-boosting techniques under the hood, there is no need to worry for any server lags.

### Extensible
The code of this tool is written in a way that makes it easy for you and your team to add new features and amazing functions - being open source, Austeritas can be maintained by a huge community in order to keep Bedrock's servers safe!
