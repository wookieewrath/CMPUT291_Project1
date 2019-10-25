import datetime
import re


def get_registration():
    regno = get_regno()

    return regno


def get_ticket_info():
    fine = get_fine()
    violation = get_violation()
    vdate = get_vdate()

    return fine, violation, vdate


def get_regno():
    regno = input("Enter the registration number: ")
    return regno


def get_fine():
    fine = input("Enter fine amount: ")

    while True:
        try:
            int(fine)
            break
        except ValueError:
            fine = input("Enter fine amount: ")

    return fine


def get_violation():
    violation = input("Enter a description of the violation: ")
    return violation


def get_vdate():
    vdate = input("Please enter violation date in YYYY-MM-DD format (include dashes): ")

    if re.match(r"\d{4}-\d{2}-\d{2}", vdate):
        return vdate
    else:
        vdate = datetime.date.today()
        return vdate.strftime("%Y-%m-%d")
