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
import login
import math

"""

(some) Issues:
    
>>> The get_marriage and get_birth do not currently use the USERS's location as the birth and marriage location
    
>>> Errors need to be caught and dealt with properly, specifically if the user enters something stupid. 
    Perhaps we can do this in the main method? Instead of catching errors in every function?
    
>>> Registry Agent function #6 needs to be completed

>>> Traffic Officer function #2 needs to be completed
    

"""

'''******************************************************************************************************
*                                      Registry Agent Function 1                                        *
******************************************************************************************************'''


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
        print("Father does not exist, creating person. Please enter details of the father:")
        new_father_input = get_new_persons.get_new_persons_parents()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (birth_input[7], birth_input[8], new_father_input[0], new_father_input[1],
                        new_father_input[2], new_father_input[3],))
        print("Father, " + birth_input[7] + ", has been added to the database.")

    if the_mother is None:
        print("Mother does not exist, creating person. Please enter details of the mother:")
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


'''******************************************************************************************************
*                                      Registry Agent Function 2                                        *
******************************************************************************************************'''


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


'''******************************************************************************************************
*                                      Registry Agent Function 3                                        *
******************************************************************************************************'''


def renew_registration(cursor):
    # Get registration number from user
    regno = get_registration_renewal.get_registration()

    # Select the expiry date of the vehicle from the database
    cursor.execute("SELECT expiry "
                   "FROM registrations "
                   "WHERE regno=?;", (regno,))
    current_expiry = (cursor.fetchone())
    if current_expiry is not None:
        current_expiry_date = datetime.datetime.strptime(current_expiry[0], "%Y-%m-%d")  # convert to datetime object

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
    else:
        print("Invalid registration number")


'''******************************************************************************************************
*                                      Registry Agent Function 4                                        *
******************************************************************************************************'''


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
        print("A new registration has been created.")


'''******************************************************************************************************
*                                      Registry Agent Function 5                                        *
******************************************************************************************************'''


def process_payment(cursor):
    # Get the desired payment amount as an integer
    info_tuple = get_ticket_payment_info.get_ticket_payment_info()
    payment_amount = int(info_tuple[2])

    # Get the fine amount from the database
    cursor.execute("SELECT * "
                   "FROM tickets "
                   "WHERE tno=?;", (info_tuple[0],))
    fine = cursor.fetchone()

    if fine is not None:
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
        if currently_paid is None and int(fine[2]) >= payment_amount:
            cursor.execute("INSERT INTO payments VALUES (?,?,?)",
                           (info_tuple[0], info_tuple[1], info_tuple[2],))
            print("A payment of " + str(payment_amount) + " was processed for ticket number: " + info_tuple[0])
        elif currently_paid is not None and int(fine[2]) >= currently_paid + payment_amount:
            new_paid = currently_paid + payment_amount
            cursor.execute("UPDATE payments SET amount=? WHERE tno=?",
                           (new_paid, info_tuple[0]))
            print("A payment of " + str(payment_amount) + " was processed for ticket number " + info_tuple[0])
        else:
            print("Invalid Payment")
    else:
        print("Invalid Ticket")


'''******************************************************************************************************
*                                      Registry Agent Function 6                                        *
******************************************************************************************************'''


def driver_abstract(cursor):

    #receiving input of names
    f_name = input("Enter first name of driver")
    l_name = input("Enter last name of driver")

    cursor.execute("SELECT * FROM persons WHERE fname = ? AND lname = ?", (f_name,l_name))
    person_exists = cursor.fetchall()

    #checking if user exists in the data base
    if len(person_exists) == 0:
        print("This user does not exist in the data base")
        return

    ordered = input("\nWould you like the tickets displayed from latest to oldest? (y/n)").lower()

    #ordering if ordering requested
    if ordered == 'y':
        cursor.execute("SELECT tickets.tno, tickets.vdate, tickets.violation, tickets.fine,tickets.regno, vehicles.make, vehicles.model FROM vehicles,tickets,registrations WHERE registrations.fname = ? AND registrations.lname = ? AND registrations.regno = tickets.regno AND vehicles.vin = registrations.vin ORDER BY date(tickets.vdate) DESC;", (f_name,l_name))
        abstract_info = cursor.fetchall()

    else:
        cursor.execute("SELECT tickets.tno, tickets.vdate, tickets.violation, tickets.fine,tickets.regno, vehicles.make, vehicles.model FROM vehicles,tickets,registrations WHERE registrations.fname = ? AND registrations.lname = ? AND registrations.regno = tickets.regno AND vehicles.vin = registrations.vin;",(f_name, l_name))
        abstract_info = cursor.fetchall()

    num_tickets = len(abstract_info)

    cursor.execute("SELECT COUNT(*), SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ?;",(f_name,l_name))
    demerits = cursor.fetchall()
    num_demerits= demerits[0][0]
    demerit_points = demerits[0][1]

    if demerit_points == None:
        demerit_points = 0

    cursor.execute("SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? AND date(ddate) >= date('now','-2 year');",(f_name,l_name))
    demerits_last_2_years = cursor.fetchall()

    if demerits_last_2_years[0][0] == None:
        demerits_last_2_years = 0

    else:
        demerits_last_2_years = demerits_last_2_years[0][0]

    print("\n%s %s has %s tickets, %s demerit notices, %s lifetime demerit points and %s demerit points in the last 2 years.\n" %(f_name,l_name,num_tickets,num_demerits,demerit_points,demerits_last_2_years))

    if num_tickets == 0:
        print("%s %s has no tickets in the database!" % (f_name,l_name))

    else:

        print("%s %s has the following tickets:\n"%(f_name,l_name))
        i = 0
        while i < num_tickets and i < 5:
            ticket_number = abstract_info[i][0]
            vio_date = abstract_info[i][1]
            vio_descript = abstract_info[i][2]
            fine = abstract_info[i][3]
            reg_num = abstract_info[i][4]
            make = abstract_info[i][5]
            model = abstract_info[i][6]
            i+=1

            print("Ticket number: %s Violation Date: %s Violation Description: %s Fine: %s Registration Number: %s Make: %s Model: %s" % (ticket_number,vio_date,vio_descript,fine,reg_num,make,model))


        if num_tickets > 5:
            more_tickets = input("%s %s has more tickets, would you like to see more? (y/n)"%(f_name,l_name)).lower()
            loops = math.ceil(num_tickets/5)
            j = 0
            while i < num_tickets:
                if more_tickets == 'y':
                    k = 0
                    while j < loops and k <5 and i < num_tickets:
                        ticket_number = abstract_info[i][0]
                        vio_date = abstract_info[i][1]
                        vio_descript = abstract_info[i][2]
                        fine = abstract_info[i][3]
                        reg_num = abstract_info[i][4]
                        make = abstract_info[i][5]
                        model = abstract_info[i][6]
                        i+=1
                        k+=1

                        print("Ticket number: %s Violation Date: %s Violation Description: %s Fine: %s Registration Number: %s Make: %s Model: %s" % (ticket_number, vio_date, vio_descript, fine, reg_num, make, model))

                elif more_tickets != 'y':
                    break

                if j < loops and i < num_tickets:
                    more_tickets = input("%s %s has more tickets, would you like to see more? (y/n)"%(f_name,l_name)).lower()


'''******************************************************************************************************
*                                     Traffic Officer Function 1                                        *
******************************************************************************************************'''


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

        print(reg_info[5] + " " + reg_info[6] + " drives a: " + vehicle_info[4] + " " + str(vehicle_info[3]) + " " +
              vehicle_info[1] + " " + vehicle_info[2])

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
            print("Congratulations comrade! You just gave " + reg_info[5] + " " + reg_info[6] + " a $" + str(
                ticket_input[0]) + " ticket for: " + ticket_input[1])

    else:
        print("No matching records.")


'''******************************************************************************************************
*                                     Traffic Officer Function 2                                        *
******************************************************************************************************'''

def find_car_owner(cursor):
    input_dictionary = {} #Will store {string_query : record_of_interest_value} pairs
    search_string = ' ' #Initializes a string which will later be used in a query searching for cars with user inputted data
    search_values = [] #A list of not-null values the user enters from the console, to be used in conjuction with the search_string
    
    #Get the relevant data about the vehicles of interest from the user
    #Add data to the dictionary as (key = relevant part of query search_string) and (value = user inputted value)
    make = input("Enter the vehicle make (Press ENTER to skip): ").strip().title()
    input_dictionary["AND make = ? "] = make
    model = input("Enter the vehicle model (Press ENTER to skip): ").strip().title()
    input_dictionary["AND model = ? "] = model
    year = input("Enter the vehicle year (Press ENTER to skip): ").strip().title()
    input_dictionary["AND year = ? "] = year
    colour = input("Enter the vehicle colour (Press ENTER to skip): ").strip().title()
    input_dictionary["AND colour = ? "] = colour
    plate = input("Enter the vehicle plate (Press ENTER to skip): ").strip()
    input_dictionary["AND plate = ? "] = plate
    
    #For every key in the dictionary representing a vehicle field, if the user did not enter a null value and skip it...
    #We add this string search field to search_string
    #We also add the (not null) user value into the search_values list
    for key in input_dictionary:
        if input_dictionary[key] != '':
            search_string = search_string + key
            search_values.append(input_dictionary.get(key))
    
    #Convert the search values list to a tuple to be syntactically used in the query
    search_values = tuple(search_values)
    
    #Execute the query with the user defined search_string and search_values
    cursor.execute("SELECT make, model, year, color, plate "
                   "FROM registrations LEFT JOIN vehicles "
                   "WHERE vehicles.vin = registrations.vin "
                   + search_string, search_values)
    
    #Store the matching rows of the database in matching_vehicles
    #vehicles_to_search = shortlist of vehicles, depending on length of matching_vehicles, we need to find owners for
    matching_vehicles = cursor.fetchall()
    vehicles_to_search = []
    
    #If there are > 4 matching vehicles, ask the user to choose a particular vehicle to find its owner
    #Add the user choice to the shortlist vehicles_to_search
    count = 0
    if len(matching_vehicles) > 4:
        for i in range(len(matching_vehicles)):
            count = count + 1
            print("VEHICLE:", count)
            print("MAKE:", matching_vehicles[i][0])
            print("MODEL:", matching_vehicles[i][1])
            print("YEAR:", matching_vehicles[i][2])
            print("COLOUR:", matching_vehicles[i][3])
            print("PLATE:", matching_vehicles[i][4], "\n")
        
        chosen_vehicle = int(input("Please enter VEHICLE NUMBER to look up: "))
        vehicles_to_search.append(matching_vehicles[(chosen_vehicle - 1)])
    
    #If there are < 4 matching vehicles, we just find the owners of all of them
    #Set the shortlist = original list (matching_vehicles)
    else:
        vehicles_to_search = matching_vehicles
    
    #For every car in the shortlist: print out the owner and their registration/vehicle details
    for i in range(len(vehicles_to_search)):
        cursor.execute("SELECT regdate, expiry, fname, lname "
                       "FROM vehicles, registrations "
                       "WHERE vehicles.vin = registrations.vin "
                       "AND make = ? AND model = ? AND year = ? AND color = ? AND plate = ?", (vehicles_to_search[i]))
        
        owner = cursor.fetchone()

        print("\nVEHICLE OWNER:", owner[2] + " " + owner[3])
        print("REGISTRATION DATE:", owner[0])
        print("EXPIRY:", owner[1])
        print("MAKE:", vehicles_to_search[i][0])
        print("MODEL:", vehicles_to_search[i][1])
        print("YEAR:", vehicles_to_search[i][2])
        print("COLOUR:", vehicles_to_search[i][3])
        print("PLATE:", vehicles_to_search[i][4])
        

'''******************************************************************************************************
*                                         Registry Agent Menu                                           *
******************************************************************************************************'''


def agent_menu(cursor, connection):
    while True:
        connection.commit()
        user_entry = input("\nSelect from one of the following options:\n"
                           "1. Register a birth\n"
                           "2. Register a marriage\n"
                           "3. Renew a vehicle registration\n"
                           "4. Process a bill of sale\n"
                           "5. Process a payment amount\n"
                           "6. Get a driver abstract\n"
                           "0. EXIT\n")

        if user_entry == "1":
            reg_birth(cursor)
        elif user_entry == "2":
            reg_marriage(cursor)
        elif user_entry == "3":
            renew_registration(cursor)
        elif user_entry == "4":
            bill_of_sale(cursor)
        elif user_entry == "5":
            process_payment(cursor)
        elif user_entry == "6":
            driver_abstract(cursor)
        elif user_entry == "0":
            break
        else:
            print("Invalid input\n")


'''******************************************************************************************************
*                                         Traffic Officer Menu                                          *
******************************************************************************************************'''


def officer_menu(cursor, connection):
    while True:
        connection.commit()
        user_entry = input("\nSelect from one of the following options:\n"
                           "1. Issue a ticket\n"
                           "2. Find a car owner\n"
                           "0. EXIT\n")

        if user_entry == "1":
            issue_ticket(cursor)
        elif user_entry == "2":
            find_car_owner(cursor)
        elif user_entry == "0":
            break
        else:
            print("Invalid input\n")


'''******************************************************************************************************
*                                              MAIN METHOD                                              *
******************************************************************************************************'''


def main():
    #query = open('prj-tables.sql', 'r').read()
    #tables = open('a2-data.sql', 'r').read()

    conn = sqlite3.connect('./testProject.db')
    cursor = conn.cursor()

    cursor.executescript('PRAGMA foreign_keys=ON;')
    # c.executescript(query)
    # c.executescript(tables)

    login_attempt = login.login(cursor)
    if login_attempt != False:
        if login_attempt == "o":
            officer_menu(cursor, conn)
        elif login_attempt == "a":
            agent_menu(cursor, conn)

    conn.commit()


if __name__ == "__main__":
    main()
