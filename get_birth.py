import datetime


def get_birth():
    fname = get_fname()
    lname = get_lname()
    regdate = get_regdate().strftime("%Y-%m-%d")
    regplace = get_regplace()
    gender = get_gender()
    f_fname = get_f_fname(fname)
    f_lname = get_f_lname(fname)
    m_fname = get_m_fname(fname)
    m_lname = get_m_lname(fname)

    return fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname


def get_fname():
    fname = input("Enter a first name: ")
    return fname


def get_lname():
    lname = input("Enter a last name: ")
    return lname


def get_regdate():
    regdate = datetime.date.today()
    return regdate


def get_regplace():
    regplace = input("Enter birth place: ")
    return regplace


def get_gender():
    while True:
        gender = input("Enter gender (M, F, or O): ")
        if gender.upper() == "M" or gender.upper() == "F" or gender.upper() == "O":
            break
    return gender


def get_f_fname(fname):
    f_fname = input("Enter " + fname + "'s father's first name: ")
    return f_fname


def get_f_lname(fname):
    f_lname = input("Enter " + fname + "'s father's last name: ")
    return f_lname


def get_m_fname(fname):
    m_fname = input("Enter " + fname + "'s mother's first name: ")
    return m_fname


def get_m_lname(fname):
    m_lname = input("Enter " + fname + "'s mother's last name: ")
    return m_lname
