import sqlite3
from User_Class import User

conn = sqlite3.connect('users.db')
c = conn.cursor()

#Right now this function will find a correct enter of username and password in the table and return that user
#If it doesn't find the username/password combination in the table it will conclude that the user doesn't exist
#PROBLEM: What if user has correct username but enters the wrong password by accident??
#SOLUTION: Implement the following 4 cases:
#1. The username and password were both found in the table -- return the user's type details
#2. The username is in the table but the password is wrong -- return ['password'] to symbolize you need to reprompt for password
#3. The password is in the table but the username is wrong -- return ['username']
#4. The username and password are not in the table -- return False to symbolize you need to create a new user
def does_user_exist(username, password):
    c.execute("SELECT uid, pwd, utype FROM users WHERE uid = ? AND pwd = ?", (username, password))
    user_in_table = c.fetchone()
    if user_in_table == None:
        return False
    else:
        return user_in_table


def create_user(uid, pwd, utype, fname, lname, city):
    c.execute("CREATE TABLE IF NOT EXISTS users(uid TEXT, pwd TEXT, utype CHAR(1), fname TEXT, lname TEXT, city TEXT)")
    
    if does_user_exist(uid, pwd) == False:
        user = User(uid, pwd, utype, fname, lname, city)
        c.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", (user.uid, user.pwd, user.utype, user.fname, user.lname, user.city))
        conn.commit()
        
    else:
        print("This user already exists inside the database!!")

create_user('Kim', 'Kim123', 'a', 'Kamillah', 'Hasham', 'Edmonton')


#You need to adjust this function because when the user puts in a wrong password... it concludes that the user doesn't exist
def login():
    username = input("Username: ")
    password = input("Password: ")
    existing_user = does_user_exist(username, password) 
    print(existing_user)
    
    if existing_user == False:
        print("This user does NOT exist... please create a user")
    
    else:
        print("This user DOES exist... her type is:" + existing_user[2])
        
login()
    
