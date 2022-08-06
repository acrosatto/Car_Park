import psycopg2
from datetime import datetime
from time import sleep


class Start:
    """Start the program. Get title and phrase to use during the program"""

    def __init__(self, phrase):
        self.phrase = phrase

    def get_title(self):
        return f'\033[37m{"==" * 30}\033[m\n{self.phrase.center(60)}\n\033[37m{"==" * 30}\033[m'

    def get_phrase(self):
        return f'\033[1;32m{self.phrase}\033[m'


class DB:
    """Connect the functions to PostgreSQL to insert, update or delete data from the tables clients and parking"""
    connection = None

    def __init__(self):
        self.host = 'localhost'
        self.dbname = 'carpark'
        self.username = 'postgres'
        self.password = 'lovepython!'
        self.port = 5432

    def connect_psql(self):
        try:
            connection = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.username,
                                          password=self.password, port=self.port)
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)


class Client:
    """Input new clients, retrieve or update info on already registered clients and get list of all clients"""

    @staticmethod
    def new_client_in():
        print()
        s = Start("NEW CLIENT")
        print(s.get_title())
        sleep(1)
        try:
            # Connecting to postgres
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM parking WHERE status = 'IN';")
            # Insert new client's info into the table clients. That will trigger the table parking to be filled
            # with: date_in, time_in and status='IN'.
            person = [(input("First Name: ").title(),
                       input("Last Name: ").title(),
                       input("Make: ").title(),
                       input("Color: "),
                       input("License Plate: "))]
            for p in person:
                cursor.execute("INSERT INTO clients("
                               "first_name, last_name, make, color, license_plate)"
                               "VALUES(%s, %s, %s, %s, %s);", p)
            print(f"\033[32m'Ready. New Client inserted successfully.'\033[m")
            print()
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mError, please try again.", "\033[m")

    @staticmethod
    def regular_client_in():
        print()
        s = Start("CLIENT")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            license_plate = [(input("License Plate: "))]
            cursor.execute("SELECT status FROM parking WHERE license_plate = %s "
                           "ORDER BY status = 'IN' DESC LIMIT 1;", license_plate)
            results = cursor.fetchone()
            for result in results:
                if result == 'OUT':
                    # Erasing the brackets in the list to add the correct license plate into the table
                    l_plate = (''.join(license_plate))

                    # generating date and time
                    now = datetime.now()
                    date_in = now.date()
                    time_in = now.strftime("%Y/%m/%d, %H:%M:%S")
                    status = 'IN'

                    # Regular client entering the car park.
                    person = [(l_plate,
                               date_in,
                               time_in,
                               status)]
                    for p in person:
                        cursor.execute("INSERT INTO parking(license_plate, date_in, time_in, status) "
                                       "VALUES(%s, %s, %s , %s);", p)
                        print(f"\033[32m'Ready. Client IN.'\033[m")
                else:
                    print("\033[31mSorry. License Plate already in the car park.\033[m\n")

            print()
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mSorry. No customer with that license plate registered in the car park.\033[m")

    @staticmethod
    def get_client_info():
        print()
        s = Start("CLIENT")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            license_plate = [(input("License Plate: "))]
            cursor.execute("SELECT status FROM parking WHERE license_plate = %s;", license_plate)
            results = cursor.fetchall()
            for result in results:
                if result:
                    cursor.execute("SELECT first_name, last_name, make, color"
                                   " FROM clients WHERE license_plate = %s;"
                                   , license_plate)

                    # Info of a client, from the table clients.
                    records = cursor.fetchmany(4)
                    print("Customer's Details:")
                    for record in records:
                        print("\033[37mFirst Name:\033[m", record[0])
                        print("\033[37mLast Name:\033[m", record[1])
                        print("\033[37mMake:\033[m", record[2])
                        print("\033[37mColor:\033[m", record[3], "\n")
                    connection.commit()

                    cursor.execute("SELECT time_in, time_out, price, status FROM parking WHERE license_plate = %s"
                                   "ORDER BY date_in DESC;"
                                   , license_plate)
                    results = cursor.fetchmany(4)
                    print("Car Park entries:")
                    for r in results:
                        print("\033[37m\t-Entry:\033[m", r[0])
                        if r[3] == 'IN':
                            print("\033[1;37m\t-Status:\033[1;32m", r[3], "\033[m", "\n")
                        else:
                            print("\033[37m\t-Out:\033[m", r[1])
                            print("\033[37m\t-Paid:\033[m$", r[2])
                            print("\033[1;37m\t-Status:\033[1;31m", r[3], "\033[m", "\n")
                    connection.commit()
                    break
            else:
                print("\033[31mNo customer with this License Plate\033[m")

            print()
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mNo customer with that license plate registered in the car park.\033[m")

    @staticmethod
    def clients_list():
        print()
        s = Start("LIST OF CLIENTS")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            # List of all the car park's clients.
            cursor.execute("SELECT * FROM clients ORDER BY customer_number;")
            results = cursor.fetchall()
            for result in results:
                print("\033[37mCustomer Number:\033[m", result[0])
                print("\033[37mFirst Name:\033[m", result[1])
                print("\033[37mLast Name:\033[m", result[2])
                print("\033[37mMake:\033[m", result[3])
                print("\033[37mColor:\033[m", result[4])
                print("\033[37mLicense Plate:\033[m", result[5])
                print("--" * 30)
            connection.commit()
            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mError, please try again.\033[m")

    @staticmethod
    def update_car_details():
        print()
        s = Start("UPDATE INFO")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            # Check if the license plate is in the system.
            old_license = [(input("Old License Plate: "))]
            cursor.execute("SELECT license_plate FROM clients WHERE license_plate = %s;", old_license)
            results = cursor.fetchone()
            if not results:
                print("\033[31mError, license plate not in the system!\033[m")
            else:
                # Erasing the brackets in the list to add the correct license plate into the table
                l_plate = (''.join(old_license))

                # Update customer's car details
                new_license = (input("New License Plate: "))
                make = (input("Make: "))
                color = (input("Color: "))

                cursor.execute("UPDATE clients SET license_plate = %s, make = %s, color = %s "
                               "WHERE license_plate = %s;", (new_license, make, color, l_plate))

                print("\033[37mUpdated successfully.\033[m")
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mError, license plate not in the system.\033[m")

    @staticmethod
    def update_customer_details():
        print()
        s = Start("UPDATE INFO")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            # Check if the license plate is in the system.
            license_plate = [(input("License Plate: "))]
            cursor.execute("SELECT license_plate FROM clients WHERE license_plate = %s;", license_plate)
            results = cursor.fetchone()
            if not results:
                print("\033[31mError, license plate not in the system!\033[m")
            else:
                # Erasing the brackets in the list to add the correct license plate into the table
                l_plate = (''.join(license_plate))

                # Update customer's details
                first_name = (input("First Name: ").title())
                last_name = (input("Last Name: ").title())

                cursor.execute("UPDATE clients SET first_name = %s, last_name = %s WHERE license_plate = %s;",
                               (first_name, last_name, l_plate))
                print("\033[37mUpdated successfully.\033[m")
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mError, license plate not in the system.\033[m")


class Management:
    """Get the amount of cars in the carpark, manage payments and get reports"""

    @staticmethod
    def get_occupancy():
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            total_lots = 15
            count_lots = 0
            cursor.execute("SELECT * FROM parking WHERE status = 'IN';")
            lots = cursor.fetchall()
            for lot in lots:
                if lot[8] == 'IN':
                    count_lots += 1
                    if total_lots - count_lots == 0:
                        print("\033[31mSorry, the carpark is full.\033[m")
            print(f"- Empty lots: \033[1;32m{total_lots - count_lots}\033[m")
            print(f"- Occupied lots: \033[1;31m{count_lots}\033[m")
            connection.commit()

            cursor.close()
            connection.close()

        except (Exception, psycopg2.Error):
            print("\033[31mError, please try again.\033[m")

    @staticmethod
    def payment():
        print()
        s = Start("CLIENT")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            license_plate = [(input("License Plate: "))]
            cursor.execute("SELECT p.status FROM parking AS p"
                           " JOIN clients AS c"
                           " ON p.license_plate = c.license_plate"
                           " WHERE p.license_plate = %s"
                           " ORDER BY p.status = 'IN' DESC LIMIT 1;", license_plate)
            results = cursor.fetchone()
            for result in results:
                if result == 'IN':
                    # Erasing the brackets in the list to add the correct license plate into the table
                    l_plate = (''.join(license_plate))

                    # Customer leaving (time)
                    status = 'IN'
                    now = datetime.now()
                    time_out = now.strftime("%Y/%m/%d, %H:%M:%S")

                    cursor.execute("UPDATE parking SET time_out = %s "
                                   "WHERE license_plate = %s AND status = %s;",
                                   (time_out, l_plate, status))

                    connection.commit()

                    # Customer leaving (day)
                    cursor.execute("UPDATE parking SET date_out = now() "
                                   "WHERE license_plate = %s AND status = %s;",
                                   (l_plate, status))
                    connection.commit()

                    # Amount of time the car stayed in the parking-lot in hours
                    cursor.execute("UPDATE parking SET time_period = ((EXTRACT(DAY FROM date_out::timestamp - "
                                   "date_in::timestamp) * (24 * 60)) + (EXTRACT(HOUR FROM time_out::time "
                                   "- time_in::time) * 60) + EXTRACT(MINUTES FROM time_out::time - time_in::time)) / 60"
                                   " WHERE license_plate=%s AND status = %s;",
                                   (l_plate, status))
                    connection.commit()
                    cursor.execute("UPDATE parking SET time_period = ROUND(time_period::numeric, 2) "
                                   "WHERE license_plate=%s AND status = %s;",
                                   (l_plate, status))
                    connection.commit()

                    # Amount to be paid: time stayed in the car park by the price $10 per hour
                    cursor.execute(
                        "UPDATE parking SET price = time_period * 10 "
                        "WHERE license_plate=%s AND status = %s;", (l_plate, status))
                    connection.commit()
                    cursor.execute("UPDATE parking SET price = ROUND(price::numeric, 2) "
                                   "WHERE license_plate=%s AND status = %s;",
                                   (l_plate, status))
                    connection.commit()

                    # Status of the customer/car IN or OUT
                    cursor.execute("UPDATE parking SET status = CASE WHEN price > 0 THEN 'OUT' ELSE 'IN' "
                                   "END WHERE license_plate = %s AND status = %s;",
                                   (l_plate, status))
                    connection.commit()

                    cursor.execute("SELECT time_period, price FROM parking WHERE license_plate = %s AND time_out = %s;",
                                   (l_plate, time_out))
                    record = cursor.fetchmany(2)
                    for r in record:
                        print(f'Parking Period: {r[0]} hours')
                        print(f'Total: ${r[1]}')
                        print("\033[32m'PAID'\033[m")
                    connection.commit()
                else:
                    print("\033[31mError. License Plate a NOT in the car park.\033[m")

            print()
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mNo customer with that license plate registered in the car park.\033[m")

    @staticmethod
    def get_cars_in_now():
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            # Report retrieved from the db table
            cursor.execute("SELECT c.first_name, c.last_name, c.make, c.color, c.license_plate,"
                           " p.time_in, p.time_out, p.time_period, p.price, p.status"
                           " FROM clients AS c"
                           " JOIN parking AS p"
                           " ON c.license_plate = p.license_plate"
                           " WHERE p.status = 'IN';")
            results = cursor.fetchall()
            print()
            for result in results:
                if result[9] == 'IN':
                    print("Client:")
                    print("\t\033[37m-First Name:\033[m", result[0])
                    print("\t\033[37m-Last Name:\033[m", result[1])
                    print("Car:")
                    print("\t\033[37m-Make:\033[m", result[2])
                    print("\t\033[37m-Color:\033[m", result[3])
                    print("\t\033[37m-License Plate:\033[m", result[4])
                    print("\033[37mDate IN:\033[m", result[5])
                    print("\033[1;37mStatus:\033[1;32m", result[9], "\033[m")
                else:
                    pass
                print("--" * 30)
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mError, please try again.\033[m")

    @staticmethod
    def get_report():
        print()
        s = Start("CAR PARK'S REPORT")
        print(s.get_title())
        sleep(1)
        try:
            connection = DB()
            connection = connection.connect_psql()
            cursor = connection.cursor()

            # Report retrieved from the db table
            from_date = input("From (YYYY/MM/DD): ")
            from_report = datetime.strptime(from_date, "%Y/%m/%d").date()
            to_date = input("To (YYYY/MM/DD): ")
            to_report = datetime.strptime(to_date, "%Y/%m/%d").date()
            cursor.execute("SELECT c.first_name, c.last_name, c.make, c.color, c.license_plate,"
                           " p.time_in, p.time_out, p.time_period, p.price, p.status"
                           " FROM clients AS c"
                           " JOIN parking AS p"
                           " ON c.license_plate = p.license_plate"
                           " WHERE p.date_in BETWEEN %s AND %s ORDER BY p.date_in;",
                           (from_report, to_report))
            results = cursor.fetchall()
            print()
            for result in results:
                print("Client:")
                print("\t\033[37m-First Name:\033[m", result[0])
                print("\t\033[37m-Last Name:\033[m", result[1])
                print("Car:")
                print("\t\033[37m-Make:\033[m", result[2])
                print("\t\033[37m-Color:\033[m", result[3])
                print("\t\033[37m-License Plate:\033[m", result[4])
                print("\033[37mDate and Time IN:\033[m", result[5])
                if result[9] == 'IN':
                    print("\033[1;37mStatus:\033[1;32m", result[9], "\033[m")
                else:
                    print("\033[37mDate and Time OUT:\033[m", result[6])
                    print("\033[37mPeriod:\033[m", result[7], "hours")
                    print("\033[37mPrice:\033[m $", result[8])
                    print("\033[1;37mStatus:\033[1;31m", result[9], "\033[m")
                print("--" * 30)

            # Amount of money made in that time period
            cursor.execute("SELECT sum(price) AS total FROM parking WHERE date_in BETWEEN %s AND %s;",
                           (from_report, to_report))
            total = cursor.fetchone()
            for t in total:
                print("\033[1;32mMoney IN: $", t, "\033[m")
            connection.commit()

            cursor.close()
            connection.close()
        except (Exception, psycopg2.Error):
            print("\033[31mError, please try again.\033[m")
