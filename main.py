import json
from os import system, name
from time import sleep
from commands import executeCmdOne, executeCmdTwo;

def readFile(name):
    f = open(name, "r")
    text = f.read()
    f.close()
    return text

#function to write to the config.json using serialization.
def writeConfig(user, email, liquid_money, notifications):
    dict = {
        "username": user,
        "email": email,
        "liquid_money": liquid_money,
        "notifications": notifications
    }
    json_object = json.dumps(dict, indent=4)
    f = open("files/config.json", "w")
    f.write(json_object)
    f.close()

#clears the screen (works on windows, linux & mac).
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

clear()

#prints the welcome-message.
print(readFile("files/trash/welcome.txt"))

# creates or edits the 'config.json' file.
def setup():
    config = json.loads(readFile("files/config.json"))
    if len(config["username"]) > 0 and len(config["email"]) > 0:
        choice = input("(yes or no) | do you want to change your config ?: ")
        if "yes" in choice:
            user = input("enter username: ")
            email = input("enter email: ")
            liquid_money = input("enter your desired amount of money: ")
            notifications = input("(yes or no) | do you want to recieve updates on your stocks ?: ")
            if "yes" in notifications:
                writeConfig(user, email, liquid_money, "true")
            else:
                writeConfig(user, email, liquid_money, "false")
    else:
        user = input("enter username: ")
        email = input("enter email: ")
        notifications = input("(yes or no) | do you want to recieve updates on your stocks ?: ")
        if "yes" in notifications:
            writeConfig(user, email, liquid_money, "true")
        else:
            writeConfig(user, email, liquid_money, "false")

setup()
sleep(1)

# prints the welcome-message & cleans the screen up.
clear()
print(readFile("files/trash/welcome.txt"))

# prints the directions on how to use the program and an input prompt.
print(readFile("files/trash/cmdInfo.txt"))
cmd = input("enter your command and its arguments: ")

#prints the welcome-message & cleans the screen up.
clear()
print(readFile("files/trash/welcome.txt"))

# loops the "command input" so that we dont need to always restart our program.
while(True):
    try:
        executeCmdTwo(cmd.split(" ")[0], cmd.split(" ")[1], cmd.split(" ")[2])
    except:
        try:
            executeCmdOne(cmd.split(" ")[0], cmd.split(" ")[1])
        except:
            print("bye bye...")

    # waits for input so that the screen doesnt get cleared instantly.
    input("...")

    # prints the welcome-message & cleans the screen up.
    clear()
    print(readFile("files/trash/welcome.txt"))

    # prints the directions on how to use the program and an input prompt.
    print(readFile("files/trash/cmdInfo.txt"))
    cmd = input("enter your command and its arguments: ")

    #prints the welcome-message & cleans the screen up.
    clear()
    print(readFile("files/trash/welcome.txt"))