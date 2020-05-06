#Created by Henry Rice


import csv
import hashlib
import random
import re
import os

salt = "salty"

def login(username, password):      # - finds the username in the csv if it exists there
                                    # - if it does exist, it checks if the password entered matches the password set for that user
                                    # - prints incorrect password if username is found but password is incorrect
                                    # - prints cant find username if a username is not found

    encrypted_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    with open('credentials.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        foundUser = False
        for row in readCSV:
            if username == row[0]:
                foundUser = True
                if row[1] == encrypted_password:
                    print("login granted:")
                    return 1
                else:
                    print("password incorrect...")
                    break

        if not (foundUser):         #tells the user if a username cant be found
            print("Cant find user with that username...")
            return 0


def get_permissions(username):      # - Goes into credentials.csv and determines usernames permissions in row[2]
                                    # - returns the permission status
    with open('credentials.csv') as csvfile:
        foundUser = False
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            if username == row[0]:
                foundUser = True
                return row[2]
        if not (foundUser):       #tells the user if a username cant be found
            print("Cant find user to get permissions for...")
            return None

def verifyPassword(password): #verifies that all password requirments are made and returns 1 if they are. If they are NOT made, return 0
    has_digit = False
    has_upper = False
    has_lower = False
    has_special = False
    has_len = False

    #check length req
    if len(password) >= 8 and len(password)<= 25:
        has_len = True
    else:
        print("password must be between 8 and 25 characters")
        return 0
    #check for digit req
    if any(x.isdigit() for x in password):
        has_digit = True
    else:
        print("password must contain a digit")
        return 0
    #check for UPPER req
    if any(x.isupper() for x in password):
        has_upper = True
    else:
        print("password must contain an Upper case letter")
        return 0
    #check for lower req
    if any(x.islower() for x in password):
        has_lower = True
    else:
        print("password must contain a lower case letter")
        return 0

    #check for special req
    specials = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if specials.search(password) != None:
        has_special = True
    else:
        print("password must contain a special character")
        return 0


    #final check if all cases satisfied
    if has_upper and has_lower and has_digit and has_special and has_len:
        return 1



def new_user():
    print("Please enter a username and password for your account...")
    new_username = input("Username: ")
    generate_pass = input("Press [y] to Generate a strong password, Press any other key to create your own password")
    if generate_pass == 'y':
        new_password = passwordGenerator()
        print("Your Generated Password is : " + new_password)
    else:
        new_password = input("Password: ")
        while (verifyPassword(new_password) == 0):
            print("Password must be between 8 and 25 characters long!")
            print("Please enter again...")
            new_password = input("Password: ")

    encrypted_pass = hashlib.sha256(salt.encode() + new_password.encode()).hexdigest()
    with open("credentials.csv",'a') as c:
        cred_line = "\n" +new_username + "," + encrypted_pass + "," + "guest"
        c.write(cred_line)

def mainMenu(username):             # - displays main menu  options
                                    # - handles user program choice
                                    # - verifies that a user has sufficient permissions to run a program
    print("-------------------MAIN-MENU-------------------")
    print("    Enter a number to access that program...")
    print("      [1] Time Reporting \n      [2] IT Helpdesk\n      [3] Accounting\n      [4] Engineering Documents ")
    programChoice = input("Please enter your choice... \n")

    if(programChoice == '1' or programChoice == '2'):   #check if the user is accessing an app that DOES NOT need permissions
        if(programChoice == '1'):
            print("You have now accessed the Time Reporting Application.")
            #Time Report Application call function here
        elif(programChoice == '2'):
            print("You have now accessed the IT Helpdesk Application.")
            #IT Helpdesk Application call function here
    elif (programChoice == '3' or programChoice == '4'):    #check if the user is accessing an app that DOES need permissions
        if(get_permissions(username)== 'admin'):
            print("Admin permissions recognized...")
            if(programChoice == '3'):
                print("You have now accessed the Accounting Application.")
                #Accounting Application call function here
            elif(programChoice == '4'):
                print("You have now accessed the Engineering Documents.")
                #Engineering Documents call function here
        elif(get_permissions(username) == 'user'):
            print("User permissions recognized...")
            if (programChoice == '3'):
                print("You have now accessed the Accounting Application.")
                #Accounting Application call function here
            elif (programChoice == '4'):
                print("You do not have sufficient permissions to access that application.")
        else:
            print("You do not have sufficient permissions to access that application.")


def runAgain(): #this function prompts the user to run the program again and returns as True (go again) or False (end the program)

    while True:
        runAgainChoice = input("Would you like to run another application? enter [y] or [n]...\n")
        if (runAgainChoice == 'y' or runAgainChoice == 'Y'):
            return True
        elif (runAgainChoice == 'n' or runAgainChoice == 'N'):
            return False
        else:
            print("please try again and enter [y] or [n]...")

def passwordGenerator():
    generated_password = ""

    lower_letters = ["a","b","c","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    upper_letters = ["A","B","C","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    digits = ["0","1","2","3","4","5","6","7","8","9"]

    for i in range(12):
        a_choice = random.randint(1,3)
        if a_choice == 1:
            generated_password += random.choice(lower_letters)
        elif a_choice == 2:
            generated_password += random.choice(upper_letters)
        elif a_choice == 3:
            generated_password += random.choice(digits)

    return generated_password

#Run Program
print("Welcome to the employee menu, please log in with username and password...")
userFound = False
login_choice_needed = True
while login_choice_needed == True:
    print("Login or Register new user:")   #ask user if they want to login or register a new user
    print("[1] Login")
    print("[2] Register")
    login_choice = input()

    if login_choice == '1':
        login_choice_needed = False         #if they choose login, go right to login process
    elif  login_choice == '2':

        new_user()
        login_choice_needed = False

while not userFound:
    print("--Login--")
    usrnm = input("Username: ")
    psswrd = input("Password: ")
    if(login(usrnm,psswrd) == 1):         #returns 1 when that user is found in credentials.csv
        userFound = True
        while True:
            mainMenu(usrnm)
            if not runAgain():
                break
        print("logging out...")

