from functions import *


title = Start("""\033[1;33m
            ╦ ╦╔═╗╦  ╔═╗╔═╗╔╦╗╔═╗  ╔╦╗╔═╗  ╔╦╗╦ ╦╔═╗  
            ║║║║╣ ║  ║  ║ ║║║║║╣    ║ ║ ║   ║ ╠═╣║╣   
            ╚╩╝╚═╝╩═╝╚═╝╚═╝╩ ╩╚═╝   ╩ ╚═╝   ╩ ╩ ╩╚═╝  
                    ╔═╗╔═╗╦═╗  ╔═╗╔═╗╦═╗╦╔═           
                    ║  ╠═╣╠╦╝  ╠═╝╠═╣╠╦╝╠╩╗           
                    ╚═╝╩ ╩╩╚═  ╩  ╩ ╩╩╚═╩ ╩           
 \033[m""")
print(title.get_title())

s = Start("OCCUPANCY NOW:")
print(s.get_phrase())
Management.get_occupancy()

spots = 15

sleep(0.5)
while True:
    print()
    s = Start("MAIN MENU")
    print(s.get_title())
    main_menu = Start('''\n\033[1;33mCAR PARK\033[m     
             [ 𝟙 ]  Clients 
             [ 𝟚 ]  Management
             [ 𝟛 ]  END Program...''')
    print(main_menu.get_phrase())
    try:
        choice = int(input("\n>>> Please choose an option: "))
        if choice == 1:
            sleep(0.5)
            while True:
                print()
                s = Start("CLIENT'S MENU")
                print(s.get_title())
                client_menu = Start('''\n\033[1;32mCLIENT\033[m     
                [ 𝟙 ]  New Client IN 
                [ 𝟚 ]  Recurring Client IN
                [ 𝟛 ]  Client OUT(payment)
                [ 𝟜 ]  Client details(check/update)
                [ 𝟝 ]  Back to MAIN MENU''')
                print(client_menu.get_phrase())
                client_choice = int(input("\n>>> Choose an option: "))
                if spots <= 0 and client_choice == 1:
                    print("\033[1;31mSorry, the carpark is full.\033[m")
                elif client_choice == 1 and spots >= 1:
                    Client.new_client_in()
                    spots -= 1
                    sleep(1)
                elif client_choice == 2 and spots <= 0:
                    print("\033[1;31mSorry, the carpark is full.\033[m")
                elif client_choice == 2 and spots >= 0:
                    Client.regular_client_in()
                    spots -= 1
                    sleep(1)
                elif client_choice == 3:
                    Management.payment()
                    spots += 1
                    sleep(1)
                elif client_choice == 4:
                    while True:
                        print()
                        s = Start("CLIENTS DETAILS")
                        print(s.get_title())
                        update_menu = Start('''\n\033[1;32mINFO\033[m 
                [ 𝟙 ]  UPDATE Client's Info
                [ 𝟚 ]  UPDATE Car's Info
                [ 𝟛 ]  Check Client's Info
                [ 𝟜 ]  Back to CLIENTS MENU''')
                        print(update_menu.get_phrase())
                        update_choice = int(input("\n>>> Choose an option: "))
                        if update_choice == 1:
                            Client.update_customer_details()
                        elif update_choice == 2:
                            Client.update_car_details()
                        elif update_choice == 3:
                            Client.get_client_info()
                        elif update_choice == 4:
                            break
                        else:
                            print("\033[31mError, try again.\033[m")
                            continue
                elif client_choice == 5:
                    break
                else:
                    print("\033[31mError, please try again.\033[m")
                    print()
                    print(" " * 15, " . " * 10, " " * 10)
                    continue
        elif choice == 2:
            sleep(0.3)
            while True:
                print()
                s = Start("MANAGEMENT'S MENU")
                print(s.get_title())
                print()
                management_menu = Start('''MANAGEMENT\033[m
                [ 𝟙 ]  Occupancy now
                [ 𝟚 ]  Report per date
                [ 𝟛 ]  Client's list
                [ 𝟜 ]  Back to MAIN MENU''')
                print(management_menu.get_phrase())
                management_choice = int(input("\n>>> Choose an option: "))
                if management_choice == 1:
                    sleep(1)
                    print()
                    s = Start("OCCUPANCY")
                    print(s.get_title())
                    Management.get_occupancy()
                    print()
                    s = Start("CARS IN NOW")
                    print(s.get_phrase())
                    Management.get_cars_in_now()
                    sleep(1)
                elif management_choice == 2:
                    sleep(1)
                    Management.get_report()
                    sleep(1)
                elif management_choice == 3:
                    Client.clients_list()
                    sleep(1)
                elif management_choice == 4:
                    break
                else:
                    print("\033[31mError, please try again.\033[m")
                    print()
                    print(" " * 15, " . " * 10, " " * 10)
                    continue
        elif choice == 3:
            fin = Start("""\033[33m
    ╔╗ ╦ ╦╔═╗┬┬┬  ╔═╗╔═╗╔╦╗╔═╗  ╔╗ ╔═╗╔═╗╦╔═  ╔═╗╔═╗╔═╗╔╗╔
    ╠╩╗╚╦╝║╣ │││  ║  ║ ║║║║║╣   ╠╩╗╠═╣║  ╠╩╗  ╚═╗║ ║║ ║║║║
    ╚═╝ ╩ ╚═╝ooo  ╚═╝╚═╝╩ ╩╚═╝  ╚═╝╩ ╩╚═╝╩ ╩  ╚═╝╚═╝╚═╝╝╚╝
""")
            print(fin.get_phrase())
            sleep(0.3)
            print("\033[32m", u"\U0001F697 ", end='')
            sleep(0.5)
            print(u"\U0001F697 ", end='')
            sleep(0.5)
            print(u"\U0001F697 ", end='')
            sleep(0.5)
            print()
            break
        else:
            print("\033[31mPlease try again...\033[m")
            print()
            print(" " * 15, " . " * 10, " " * 10)
    except ValueError:
        print("\033[31mPlease enter a valid number...\033[m")
        print()
        print(" " * 15, " . " * 10, " " * 10)
