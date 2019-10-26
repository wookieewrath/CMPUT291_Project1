import re


def get_new_persons():
    fname = get_fname()
    lname = get_lname()
    bdate = get_bdate()
    bplace = get_bplace()
    address = get_address()
    phone = get_phone()

    return fname, lname, bdate, bplace, address, phone


# For register a birth function
def get_new_persons_parents():
    bdate = get_bdate()
    bplace = get_bplace()
    address = get_address()
    phone = get_phone()

    return bdate, bplace, address, phone


def get_fname():
    fname = input("Enter the new person's first name: ")
    return fname


def get_lname():
    lname = input("Enter the new person's last name: ")
    return lname


def get_bdate():
    bdate = input("Enter the new person's birth date in YYYY-MM-DD format (include dashes): ")

    while True:
        if re.match(r"\d{4}-\d{2}-\d{2}", bdate):
            break
        else:
            print("Please enter in YYYY-MM-DD format: ")
            bdate = input("Enter the new person's birth date in YYYY-MM-DD format (include dashes): ")

    return bdate


def get_bplace():
    bplace = input("Enter new person's birth place: ")
    return bplace


def get_address():
    address = input("Enter the new person's address: ")
    return address


def get_phone():
    phone = input("Enter the new person's phone number in ###-###-### format (include dashes): ")

    while True:
        if re.match(r"\d{3}-\d{3}-\d{4}", phone):
            break
        else:
            print("Please enter in ###-###-#### format: ")
            phone = input("Enter the new person's phone number in ###-###-### format (include dashes): ")

    return phone
