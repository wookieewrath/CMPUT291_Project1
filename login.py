import sqlite3
import datetime
import random
import sqlite3

from get_new_persons import get_new_persons


#Obtain the username and password from the console.
#Return [username, password].
def get_login_details():
    username = input("Username: ")
    password = input("Password: ")
    return [username, password]


#This function will check whether the user exists or doesn't exist based on the username and password.
#If the username and password were entered in correctly: return (username, password, type).
#If the user misspells the password: return True.
#If the user does not exist: return False.
def does_user_exist(username, password, c):
    #Find the username password combination in the table.
    c.execute("SELECT uid, pwd, utype, city FROM users WHERE uid = ? AND pwd = ?", (username, password))
    user_in_table = c.fetchone()
    
    #If the username and password were entered correctly we return that user. 
    if user_in_table != None:
        return user_in_table
    
    #If we did not find an exact username and password combination...
    else:
        #Find the username somewhere in the table.
        c.execute("SELECT uid FROM users WHERE uid = ?", (username,))
        matching_usernames = c.fetchall()
        
        #If either the username exists somewhere, we conclude that the user exists and there was just a console spelling error.
        if (len(matching_usernames) > 0):
            return True
        
        #If the username doesn't exist anywhere inside the table, we concluse that the user doesn't exist.
        else:
            return False
           
            
#This function creates a user and adds it to the database.         
def create_user(uid, pwd, utype, fname, lname, city, c):
    c.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", (uid, pwd, utype, fname, lname, city))
    
    
#This function will provide the login menu for the program.
#False return value means login was not successful.
#User type return value when login was successful.
def login(c):
    #Ask the user to enter their username and password.
    login_details = get_login_details()
    username = login_details[0]
    password = login_details[1]
    
    #Check is these credentials correspond to an existing user.
    existing_user = does_user_exist(username, password, c) 
    
    #If the user exists inside the table, there was a spelling error.
    if existing_user == True:
        return False
        
    #If the user doesn't exist in the table, provide the option to create a user with those credentials.
    elif existing_user == False:
        create = input("This user does not exist. Do you want to create a user? yes/no: ").strip().lower()
        if create == 'yes':
            personal_details = get_new_persons()
            login_information = get_login_details()
            fname = personal_details[0]
            lname = personal_details[1]
            bdate = personal_details[2]
            bplace = personal_details[3]
            address = personal_details[4]
            phone_number = personal_details[5]
            uname = login_information[0]
            passw = login_information[1]
            utype = input("Is " + uname + " a traffic officer or a registry agent? o/a: ").strip().lower()
            city = input("What city does this user operate in? ").strip().title()
            c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?)", (fname, lname, bdate, bplace, address, phone_number))
            create_user(uname, passw, utype, fname, lname, city, c)
        return False
            
    #If the credentials were entered in correctly, return the type of the user.
    #Return 'a' for agent or 'o' for officer.
    else:
        return [existing_user[2], existing_user[3]]
