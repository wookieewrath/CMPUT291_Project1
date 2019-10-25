class User:
    
    def __init__(self, username, password, user_type, first_name, last_name, city):
        self.uid = username
        self.pwd = password
        self.utype = user_type
        self.fname = first_name
        self.lname = last_name
        self.city = city