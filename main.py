import datetime
import random
import sqlite3

import get_birth
import get_marriage
import get_new_persons
import get_process_sale
import get_registration_renewal
import get_ticket_payment_info
import get_issue_ticket

"""

(some) Issues:
    
>>> The get_marriage and get_birth do not currently use the USERS's location as the birth and marriage location

>>> A main menu/UI should be implemented......
    Currently, there is no login, and no interface prompting the user for different actions.
    
>>> Errors need to be caught and dealt with properly, specifically if the user enters something stupid. 
    Perhaps we can do this in the main method? Instead of catching errors in every function?
    

"""

'''******************************Looks completed, testing required******************************'''
'''Registry agent function 1'''

def reg_birth(cursor):

    # Generate a random regno that is not in the database
    cursor.execute("SELECT regno FROM births;")
    list_of_birth_registrations = [row[0] for row in (cursor.fetchall())]
    while True:
        new_regno = random.randint(100, 999)
        if new_regno not in list_of_birth_registrations:
            break

    # Get the info for the newly birth'd person
    birth_input = get_birth.get_birth()
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (birth_input[7], birth_input[8],))
    the_father = cursor.fetchone()
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (birth_input[9], birth_input[10],))
    the_mother = cursor.fetchone()

    # Check if the father and mother exist, if not create them
    if the_father is None:
        print("Father does not exist, creating person.")
        new_father_input = get_new_persons.get_new_persons_parents()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (birth_input[7], birth_input[8], new_father_input[0], new_father_input[1],
                        new_father_input[2], new_father_input[3],))
        print("Father, " + birth_input[7] + ", has been added to the database.")

    if the_mother is None:
        print("Mother does not exist, creating person.")
        new_mother_input = get_new_persons.get_new_persons_parents()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (birth_input[9], birth_input[10], new_mother_input[0], new_mother_input[1],
                        new_mother_input[2], new_mother_input[3],))
        print("Mother, " + birth_input[9] + ", has been added to the database as a new person.")

    # Re-select the father and mother from the database
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (birth_input[7], birth_input[8],))
    the_father = cursor.fetchone()
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (birth_input[9], birth_input[10],))
    the_mother = cursor.fetchone()

    # Enter the new person into the persons table
    cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                   (birth_input[0], birth_input[1], birth_input[2], birth_input[3],
                    the_mother[4], the_mother[5],))

    # Enter the new person into the births table
    cursor.execute("INSERT INTO births VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (new_regno, birth_input[0], birth_input[1], birth_input[4], birth_input[5],
                    birth_input[6], the_father[0], the_father[1], the_mother[0], the_mother[1],))

    print(birth_input[0] + " " + birth_input[1] + " is born!!!")


'''******************************Looks completed, testing required******************************'''
'''Registry agent function 2'''
def reg_marriage(cursor):
    # Generate a random regno that is not in the database
    cursor.execute("SELECT regno FROM marriages;")
    list_of_marriage_registrations = [row[0] for row in (cursor.fetchall())]
    while True:
        new_regno = random.randint(100, 999)
        if new_regno not in list_of_marriage_registrations:
            break
    # Generate today's date in the proper format
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Get detail's of marriage from the user
    marriage_input = get_marriage.get_marriage()

    # Find the existing persons (if they exist) from the database
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (marriage_input[2], marriage_input[3],))
    person1 = cursor.fetchone()
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (marriage_input[4], marriage_input[5],))
    person2 = cursor.fetchone()

    # If either person does not exist, create them
    if person1 is None:
        print("Person 1 not found, creating new person. Please enter details: ")
        person1_details = get_new_persons.get_new_persons()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (person1_details[0], person1_details[1], person1_details[2], person1_details[3],
                        person1_details[4], person1_details[5],))
        cursor.execute("SELECT * "
                       "FROM persons "
                       "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                       (person1_details[0], person1_details[1],))
        person1 = cursor.fetchone()
    if person2 is None:
        print("Person 2 not found, creating new person. Please enter details: ")
        person2_details = get_new_persons.get_new_persons()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (person2_details[0], person2_details[1], person2_details[2], person2_details[3],
                        person2_details[4], person2_details[5],))
        cursor.execute("SELECT * "
                       "FROM persons "
                       "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                       (person2_details[0], person2_details[1],))
        person2 = cursor.fetchone()

    # Register the marriage
    cursor.execute("INSERT INTO marriages VALUES (?,?,?,?,?,?,?)",
                   (new_regno, today, marriage_input[1], person1[0], person1[1], person2[0], person2[1],))

    print("Congratulations!!! " + person1[0] + " and " + person2[0] + " are now a happily married couple.")


'''******************************Looks completed, testing required******************************'''
'''Registry agent function 3'''
def renew_registration(cursor):
    # Get registration number from user
    regno = get_registration_renewal.get_registration()

    # Select the expiry date of the vehicle from the database
    cursor.execute("SELECT expiry "
                   "FROM registrations "
                   "WHERE regno=?;", (regno,))
    current_expiry = (cursor.fetchone())[0]
    current_expiry_date = datetime.datetime.strptime(current_expiry, "%Y-%m-%d")  # convert to datetime object

    # if already expired, or expires today, then new expiry is one year from today
    # if not yet expired, update the expiry to one year plus the current expiry date
    if current_expiry_date.date() <= (datetime.date.today()):
        next_year = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        cursor.execute("UPDATE registrations "
                       "SET expiry=? "
                       "WHERE regno=?", (next_year, regno,))
    else:
        next_year = (current_expiry_date + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        cursor.execute("UPDATE registrations "
                       "SET expiry=? "
                       "WHERE regno=?", (next_year, regno,))

    print("The registration has been renewed")


'''******************************Looks completed, testing required******************************'''
'''Registry agent function 4'''
def bill_of_sale(cursor):
    # Retrieve the current registration info using the users input
    info_tuple = get_process_sale.get_sale_info()
    cursor.execute(
        "SELECT * "
        "FROM registrations "
        "WHERE vin=? COLLATE NOCASE AND fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE "
        "ORDER BY regdate DESC",
        (info_tuple[0], info_tuple[1], info_tuple[2]))
    registration_info = cursor.fetchone()

    # Retrieve the info of the new owner
    cursor.execute("SELECT * "
                   "FROM persons "
                   "WHERE fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
                   (info_tuple[3], info_tuple[4],))
    new_owner_info = cursor.fetchone()

    # If no matches found, do nothing
    if registration_info is None:
        print("No matching entries found")
    else:
        # Create string representations of today's date, and the date a year from today
        today = datetime.date.today().strftime("%Y-%m-%d")
        next_year = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")

        # Set the old registration to expire today
        cursor.execute(
            "UPDATE registrations "
            "SET expiry=? "
            "WHERE vin=? AND fname=? COLLATE NOCASE AND lname=? COLLATE NOCASE",
            (today, registration_info[4], registration_info[5], registration_info[6]))

        # Create a new registration with the inputted new owner's name and new plate
        # Generate a random registration number that does not currently exist in the database
        cursor.execute("SELECT regno "
                       "FROM registrations;")
        list_of_registrations = [row[0] for row in (cursor.fetchall())]
        while True:
            new_regno = random.randint(100, 999)
            if new_regno not in list_of_registrations:
                break
        cursor.execute("INSERT INTO registrations VALUES (?,?,?,?,?,?,?)",
                       (new_regno, today, next_year, info_tuple[5], registration_info[4], new_owner_info[0],
                        new_owner_info[1],))
        print("A new registration has been created")


'''******************************Looks completed, testing required******************************'''
'''Registry agent function 5'''
def process_payment(cursor):
    # Get the desired payment amount as an integer
    info_tuple = get_ticket_payment_info.get_ticket_payment_info()
    payment_amount = int(info_tuple[2])

    # Get the fine amount from the database
    cursor.execute("SELECT * "
                   "FROM tickets "
                   "WHERE tno=?;", (info_tuple[0],))
    fine = int(cursor.fetchone()[2])

    # Get the payments until now (if they exist) from the database
    cursor.execute("SELECT amount "
                   "FROM payments "
                   "WHERE tno=?;", (info_tuple[0],))

    currently_paid = cursor.fetchone()
    if currently_paid is None:
        pass
    else:
        currently_paid = int(currently_paid[0])

    # If there are no payments yet, and the fine>=desired_payment, insert into payments
    # If there are payments, and the fine>=desired_payment+payments_until_now, update the payments table
    # Else, the payment is invalid
    if currently_paid is None and fine >= payment_amount:
        cursor.execute("INSERT INTO payments VALUES (?,?,?)",
                       (info_tuple[0], info_tuple[1], info_tuple[2],))
        print("A payment of " + str(payment_amount) + " was processed for ticket number: " + info_tuple[0])
    elif currently_paid is not None and fine >= currently_paid + payment_amount:
        new_paid = currently_paid + payment_amount
        cursor.execute("UPDATE payments SET amount=? WHERE tno=?",
                       (new_paid, info_tuple[0]))
        print("A payment of " + str(payment_amount) + " was processed for ticket number " + info_tuple[0])
    else:
        print("Invalid Payment")


'''******************************Incomplete******************************'''
'''Registry agent function 6'''
def driver_abstract():
    pass


'''******************************Looks completed, testing required******************************'''
'''Traffic officer function 1'''
def issue_ticket(cursor):
    regno_input = get_issue_ticket.get_registration()
    cursor.execute("SELECT * "
                   "FROM registrations "
                   "WHERE regno=?;", (regno_input,))
    reg_info = cursor.fetchone()

    if reg_info is not None:
        cursor.execute("SELECT * "
                       "FROM vehicles "
                       "WHERE vin=?;", (reg_info[4],))
        vehicle_info = cursor.fetchone()

        print(reg_info[5] + " " + reg_info[6] + " drives a: " + vehicle_info[4] + " " + str(vehicle_info[3]) + " " + vehicle_info[1] + " " + vehicle_info[2])

        give_ticket = input("Would you like to give " + reg_info[5] + " " + reg_info[6] + " a ticket? (Y/N): ")

        if give_ticket.lower() == "y":
            cursor.execute("SELECT tno FROM tickets;")
            list_of_tno = [row[0] for row in (cursor.fetchall())]
            while True:
                new_tno = random.randint(100, 999)
                if new_tno not in list_of_tno:
                    break
            ticket_input = get_issue_ticket.get_ticket_info()
            cursor.execute("INSERT INTO tickets VALUES (?,?,?,?,?)",
                           (new_tno, reg_info[0], ticket_input[0], ticket_input[1], ticket_input[2]))
            print("Congratulations comrade! You just gave " + reg_info[5] + " " + reg_info[6] + " a $" + str(ticket_input[0]) + " ticket for: " + ticket_input[1])

    else:
        print("No matching records.")


'''******************************Incomplete******************************'''
'''Traffic officer function 2'''
def find_car_owner():
    pass



def main():
    query = open('prj-tables.sql', 'r').read()
    tables = open('a2-data.sql', 'r').read()

    conn = sqlite3.connect('./testProject.db')
    c = conn.cursor()

    c.executescript('PRAGMA foreign_keys=ON;')
    # c.executescript(query)
    # c.executescript(tables)

    process_payment(c)

    conn.commit()


if __name__ == "__main__":
    main()

