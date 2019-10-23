def get_sale_info():
    vin = get_vin()
    old_fname = get_old_fname()
    old_lname = get_old_lname()
    new_fname = get_new_fname()
    new_lname = get_new_lname()
    new_plate = get_new_plate()

    return vin, old_fname, old_lname, new_fname, new_lname, new_plate


def get_vin():
    vin = input("Enter the vin: ")
    return vin


def get_old_fname():
    old_fname = input("Enter the current owner's first name: ")
    return old_fname


def get_old_lname():
    old_lname = input("Enter the current owner's last name: ")
    return old_lname


def get_new_fname():
    new_fname = input("Enter the new owner's first name: ")
    return new_fname


def get_new_lname():
    new_lname = input("Enter the new owner's last name: ")
    return new_lname


def get_new_plate():
    new_plate = input("Enter the new plate number: ")
    return new_plate
