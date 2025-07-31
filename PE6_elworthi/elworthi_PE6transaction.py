# Eric Worthington, CIS345, A3

import json
import os.path
import random
import csv
import time
import elworthi_PE6logger
import statistics

try:
    with open('customers.json', 'r') as file:
        accounts = json.load(file)
except FileNotFoundError:
    accounts = {}

def log_transactions(transactions):
    file = os.path.isfile("elworthi_A3transaction.py")
    with open("transaction.csv", "a", newline='') as fp:
        data = csv.writer(fp)
        if not file:
            data.writerow(["Data Time", "Username", "Old Balance", "Amount", "New Balance"])
        for transaction in transactions:
            data.writerow([
                transaction["Data Time"],
                transaction["Username"],
                transaction["Old Balance"],
                transaction["Amount"],
                transaction["New Balance"]
            ])

def save_accounts():
    with open('customers.json', 'w') as file:
        json.dump(accounts, file)

def create_new_account():
    username = input("Enter username: ")
    if username in accounts:
        print("Username already exists.")
        return

    pin = int(input('Enter 1 to create a pin yourself or 2 and the system will create a pin for you: '))
    if pin == 1:
        pin = elworthi_PE6logger.create_pin()
    else:
        pin = random.randint(1, 9999)
        print(f"Your pin is: {pin}")

    name = input("Please enter your name: ")

    try:
        checking_deposit = float(input("Enter first deposit amount to checking account: "))
        if checking_deposit < 0:
            raise ValueError("Invalid number entered. The current balance will be 0.0")
    except(ValueError, TypeError) as ex:
        print("Invalid number entered. The current balance will be 0.0")
        checking_deposit = 0.0

    try:
        saving_deposit = float(input("Enter first deposit amount to saving account: "))
        if saving_deposit < 0:
            raise ValueError("Invalid number entered. The current balance will be 0.0")
    except(ValueError, TypeError) as ex:
        print("Invalid number entered. The current balance will be 0.0")
        saving_deposit = 0.0

    accounts[username] = {
        "Pin": pin,
        "Name": name,
        "C": checking_deposit,
        "S": saving_deposit,}

    print("Account successfully created.")

def make_transactions(username):
    if username in accounts:
        print("Cactus Bank - Making Transactions\n")
        attempts = 0
        while attempts < 3:
            transaction = input("Enter pin or x to exit the application: ")
            if transaction == str(accounts[username]['Pin']):
                print(f"Welcome {accounts[username]['Name']}")
                print(f"{'Select Account':^20}")
                bank_account = input("Enter C or S for (C)hecking or (S)avings: ").upper()
                print(f"Opening {bank_account} Account...\n")

                print('Transaction instructions:')
                print(' - Withdrawal enter a negative dollar amount: -20.00.')
                print(' - Deposit enter a positive dollar amount: 10.50\n\n')

                print(f"Current Balance: ${accounts[username][bank_account]}")

                transactions = []
                while True:
                    try:
                        amount = float(input(f'Enter transaction amount: '))
                    except (ValueError, TypeError) as ex:
                        print(f'Error: {ex}. Bad Amount - No Transaction.')

                    old_balance = accounts[username][bank_account]
                    new_balance = old_balance + amount

                    transactions.append({
                        "Data Time": time.strftime("%a %b %d %H:%M:%S %Y"),
                        "Username": username,
                        "Old Balance": old_balance,
                        "Amount": amount,
                        "New Balance": new_balance
                    })

                    accounts[username][bank_account] =new_balance
                    print(f"Transaction complete. New balance is ${new_balance}")

                    cont = input("Press n to make another transaction or x to exit application: ").lower()
                    if cont == 'x':
                        log_transactions(transactions)
                        return
                    elif cont != 'n':
                        print("Invalid input. Please enter 'n' to make another transaction or 'x' to exit.")
            else:
                attempts += 1
                print(f"Invalid pin. Attempt {attempts} of 3. Please try again.")
                if attempts == 3:
                    response = input(" Do you want to get a new pin (y/n)? ").casefold()
                    if response == 'y':
                        accounts[username]["Pin"] = elworthi_PE6logger.create_pin()
                        print("Please visit the system again to make a transaction.")
                        input("Press enter to continue....")
                    else:
                        print("Exiting application")
                        return

                save_accounts()

    else:
        print("Username not found.")

def delete_account(username):
    if username in accounts:
        del accounts[username]
        print("Account deleted successfully.")
    else:
        print("Account not found.")

def print_records():
    print("Saving data...\n")
    print("Data Saved.")
    print("Exiting...")

    for username, data in accounts.items():
        print(f"{username: >10} {data['Pin']: >10} {data['Name']: >25} {data['C']: >20} {data['S']: >20}")

def checking_average():
    checking_balance = [data["C"] for data in accounts.values()]
    avg_checking = statistics.mean(checking_balance)

    print(f"\nChecking accounts' average is ${avg_checking}")
    print(f"Customers whose checking account balance is above the average:")
    for username, data in accounts.items():
        if data["C"] > avg_checking:
            print(f"username is {username} and name is {data['Name']}")

def saving_average():
    saving_balance = [data["S"] for data in accounts.values()]
    avg_saving = statistics.mean(saving_balance)

    print(f"\nSaving accounts' average is ${avg_saving}")
    print(f"Customers whose saving account is above the average:")
    for username, data in accounts.items():
        if data["S"] > avg_saving:
            print(f"username is {username} and name is {data['Name']}")

# Main program loop
while True:
    print(f'{"Welcome to Cactus Bank!":}')
    print(f"{'*' * 33}")
    print("* Enter 1 to add a new customer *")
    print("* Enter 2 to delete a customer  *")
    print("* Enter 3 to make transactions  *")
    print("* Enter 4 to exit               *")
    print(f"{'*' * 33}\n")

    selection = input("Enter your choice: ")

    if selection == '1':
        create_new_account()
        save_accounts()
        print("Exiting program.")
        print_records()
        checking_average()
        saving_average()
        exit()
    elif selection == '2':
        username = input("Enter username to delete: ")
        delete_account(username)
        save_accounts()
        print("Exiting program.")
        print_records()
        checking_average()
        saving_average()
        exit()
    elif selection == '3':
        username = input("Enter username: ")
        make_transactions(username)
        save_accounts()
        print("Exiting program.")
        print_records()
        checking_average()
        saving_average()
        exit()
    elif selection == '4':
        print("Exiting program.")
        print_records()
        checking_average()
        saving_average()
        exit()
    else:
        print("Invalid selection. Please try again.")
