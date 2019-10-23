import datetime
import random
import sqlite3

import get_birth
import get_process_sale
import get_registration_renewal
import get_ticket_payment_info

"""
(some) Issues;
1. Queries, (in particular, updates and insertions) are not case-insensitive
2. The reg_birth method needs to:
    > add a new person in the 'persons' table,
    > prompt for parent's name if not in database, and create those persons
    
3. The get_marriage and get_birth do not currently use the user's location as the birth and marriage location

4. A main menu/UI should be implemented......
    Currently, there is no login, and no interface prompting the user for different actions.

"""

def reg_birth(cursor):
    cursor.execute("SELECT regno FROM births;")
    list_of_birth_registrations = [row[0] for row in (cursor.fetchall())]
    while True:
        new_regno = random.randint(100, 999)
        if new_regno not in list_of_birth_registrations:
            break
    entry = get_birth.get_birth()
    cursor.execute("INSERT INTO births VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (new_regno, entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7],
                    entry[8],))


def renew_registration(cursor):
    # Get registration number from user
    regno = get_registration_renewal.get_registration()

    # Select the expiry date of the vehicle from the database
    cursor.execute("SELECT expiry FROM registrations WHERE regno=?;", (regno,))
    current_expiry = (cursor.fetchone())[0]
    current_expiry_date = datetime.datetime.strptime(current_expiry, "%Y-%m-%d")  # convert to datetime object

    # if already expired, or expires today, then new expiry is one year from today
    # if not yet expired, update the expiry to one year plus the current expiry date
    if current_expiry_date.date() <= (datetime.date.today()):
        next_year = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        cursor.execute("UPDATE registrations SET expiry=? WHERE regno=?", (next_year, regno,))
    else:
        next_year = (current_expiry_date + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        print(next_year)
        cursor.execute("UPDATE registrations SET expiry=? WHERE regno=?", (next_year, regno,))


def bill_of_sale(cursor):
    # Retrieve info from user and execute the search query
    info_tuple = get_process_sale.get_sale_info()
    cursor.execute("SELECT * FROM registrations WHERE vin=? COLLATE NOCASE AND fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (info_tuple[0], info_tuple[1], info_tuple[2]))
    current_info = (cursor.fetchone())
    print(current_info)

    # If no matches found, do nothing
    if current_info is None:
        print("No matching entries found")
    else:
        # Create string representations of today's date, and the date a year from today
        today = datetime.date.today().strftime("%Y-%m-%d")
        next_year = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")

        # Set the old registration to expire today
        cursor.execute("UPDATE registrations SET expiry=? WHERE vin=? AND fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                       (today, info_tuple[0], info_tuple[1], info_tuple[2]))

        # Create a new registration with the inputted new owner's name and new plate
        # Generate a random registration number that does not currently exist in the database
        cursor.execute("SELECT regno FROM registrations;")
        list_of_registrations = [row[0] for row in (cursor.fetchall())]
        while True:
            new_regno = random.randint(100, 999)
            if new_regno not in list_of_registrations:
                break
        cursor.execute("INSERT INTO registrations VALUES (?,?,?,?,?,?,?) COLLATE NOCASE",
                       (new_regno, today, next_year, info_tuple[5], info_tuple[0], info_tuple[3], info_tuple[4]))


def process_payment(cursor):
    # Get the desired payment amount as an integer
    info_tuple = get_ticket_payment_info.get_ticket_payment_info()
    payment_amount = int(info_tuple[2])

    # Get the fine amount from the database
    cursor.execute("SELECT * FROM tickets WHERE tno=?;", (info_tuple[0],))
    fine = int(cursor.fetchone()[2])

    # Get the payments until now (if they exist) from the database
    cursor.execute("SELECT amount FROM payments WHERE tno=?;", (info_tuple[0],))
    currently_paid = int(cursor.fetchone()[0])

    # If there are no payments yet, and the fine>=desired_payment, insert into payments
    # If there are payments, and the fine>=desired_payment+payments_until_now, update the payments table
    # Else, the payment is invalid
    if currently_paid is None and fine >= payment_amount:
        cursor.execute("INSERT INTO payments VALUES (?,?,?)",
                       (info_tuple[0], info_tuple[1], info_tuple[2],))
    elif currently_paid is not None and fine >= currently_paid + payment_amount:
        new_paid = currently_paid + payment_amount
        cursor.execute("UPDATE payments SET amount=? WHERE tno=?",
                       (new_paid, info_tuple[0]))
    else:
        print("Invalid Payment")


def main():
    query = open('prj-tables.sql', 'r').read()
    tables = open('a2-data.sql', 'r').read()

    conn = sqlite3.connect('./testProject.db')
    c = conn.cursor()

    c.executescript('PRAGMA foreign_keys=ON;')
    # c.executescript(query)
    # c.executescript(tables)

    bill_of_sale(c)

    conn.commit()


if __name__ == "__main__":
    main()
