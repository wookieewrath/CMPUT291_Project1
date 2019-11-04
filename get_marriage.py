import datetime


def get_marriage():
    regdate = get_regdate().strftime("%Y-%m-%d")
    regplace = get_regplace()
    p1_fname = get_p1_fname()
    p1_lname = get_p1_lname()
    p2_fname = get_p2_fname()
    p2_lname = get_p2_lname()

    return regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname


def get_regdate():
    regdate = datetime.date.today()
    return regdate


def get_regplace():
    print("Agent's city will be used for registration place")
    return None


def get_p1_fname():
    p1_fname = input("Enter the first partner's first name: ")
    return p1_fname


def get_p1_lname():
    p1_lname = input("Enter the first partner's last name: ")
    return p1_lname


def get_p2_fname():
    p2_fname = input("Enter the second partner's first name: ")
    return p2_fname


def get_p2_lname():
    p2_lname = input("Enter the second partner's last name: ")
    return p2_lname
