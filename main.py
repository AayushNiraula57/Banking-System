from user import User, NormalUser, AdminUser
from account_manager import AccountJSONManager
from account import Account
from helper import Helper
from enum import Enum
import getpass


class File(Enum):
    USER = "user.json"
    ACCOUNT = "account.json"


# Get account for logged-in user
def get_account(account_number, account_name):
    account_manager = AccountJSONManager(File.ACCOUNT.value)
    accounts = account_manager.load_accounts()
    target_account = None
    if len(accounts) == 0:
        accounts.append(Account(name=account_name, account_number=account_number))
    else:
        for account in accounts:
            acc_num = account.get_account_number()
            if acc_num == account_number:
                target_account = account
                accounts.append(Account(name=account_name, balance=target_account.get_balance(),
                                        transactions=target_account.get_transactions(),
                                        account_number=account_number))
                break
            else:
                accounts.append(Account(name=account_name, account_number=account_number))
    return accounts


def signup_menu():
    print('\n')
    print(" ------------Banking System----------------- ")
    print("1. Login \t \t 2. Register \t \t 3. Exit")
    print("--------------------------------------------")

    option = input("Enter your choice: ")
    return option


def perform_signup(option):
    while True:
        back = False
        match option:
            case '1':
                while True:
                    print("\n")
                    account_email = input("Enter Email: ")
                    password = getpass.getpass(prompt='Input the Password:')
                    user = User(account_email, password)
                    is_logged_in, user = user.login(File.USER.value)
                    if is_logged_in:
                        print("!!-----Logged in Successfully------!!")
                        # Initialize account for user
                        account_email, account_name, account_number = user.get_details()
                        accounts = get_account(account_number, account_name)
                        is_admin = False
                        if user.get_role() == "Admin":
                            # Initialize AdminUser Instance
                            is_admin = True
                            a_email, a_name, a_acc_num = user.get_details()
                            user = AdminUser(a_email, a_name, password)
                            user.__account_number = a_acc_num
                        return back, accounts, user, is_admin
                    print("\n")
                    print("1. Continue \t \t 2. Go Back")
                    value = input("Enter your choice: ")
                    if value == '2':
                        back = True
                        return back, None, user, False

            case '2':
                while True:
                    account_email = input("Enter Email: ")
                    is_email_valid = Helper.check_email(account_email)
                    if not is_email_valid:
                        continue
                    account_name = input("Enter Name: ")
                    is_valid_name = Helper.check_name(account_name)
                    if not is_valid_name:
                        continue
                    password = getpass.getpass(prompt='Input the Password:')
                    is_valid_password = Helper.check_password(password)
                    if not is_valid_password:
                        continue
                    user = NormalUser(account_email, password, account_name)
                    registered, user = user.register(File.USER.value)
                    if registered:
                        account_email, account_name, account_number = user.get_details()
                        accounts = get_account(account_number, account_name)
                        back = True
                        is_admin = False
                        if user.get_role() == "Admin":
                            is_admin = True
                            a_email, a_name, a_acc_num = user.get_details()
                            user = AdminUser(a_email, a_name, password)
                            user.__account_number = a_acc_num
                        return back, accounts, user, is_admin

                    print("1. Continue \t \t 2. Go Back")
                    value = input("Enter your choice: ")
                    if value == '2':
                        back = True
                        accounts = None
                        user = None
                        is_admin = False
                        return back, accounts, user, is_admin

            case '3':
                exit()
            case _:
                print("!!-------Invalid choice-------!!")
                back = True
                accounts = None
                user = None
                is_admin = False
                return back, accounts, user, is_admin


# Display menu and process user input
def display_menu():
    print('\n')
    print("**-----------------**Choose any option**-------------------**")
    print("1. Deposit Amount \t \t 2. Withdraw Amount")
    print("3. View Transaction History \t 4. View Transaction Statistics")
    print("5. Logout  \t \t \t 6. Exit")
    print("**---------------------------------------------------------**")
    print('\n')

    option = input("Enter your choice: ")
    return option


# Display menu and process user input
def admin_menu():
    print('\n')
    print("**-----------------**Choose any option**-------------------**")
    print("1. View Users \t \t 2. Delete Users \t \t 3. Exit" )
    print("**---------------------------------------------------------**")
    print('\n')

    option = input("Enter your choice: ")
    return option


# Perform actions based on user choice
def perform_admin_action(choice,user):
    match choice:
        case '1':  # View Users
            user.view_users(File.USER.value)
        case '2':  # Delete Users
            print("Delete User")
            user.view_users(File.USER.value)
            index = input("Enter account number: ")
            user.delete_user(index, File.USER.value)
        case '3':  # Exit
            exit()
        case _:
            print("Invalid choice")


# Perform actions based on user choice
def perform_action(choice, account, account_manager):
    match choice:
        case '1':  # Deposit
            amount = input("Enter transaction amount: ")
            if Helper.is_amount_valid(amount):
                description = input("Enter transaction description: ")
                account.deposit(float(amount), description, account_manager)
        case '2':  # Withdraw
            amount = input("Enter transaction amount: ")
            if Helper.is_amount_valid(amount):
                description = input("Enter transaction description: ")
                account.withdraw(float(amount), description, account_manager)
        case '3':  # Transaction History
            print("**-------** Transaction History: **--------**")
            print("Amount \t\t Type \t\t Time \t\t Description")
            for transaction in transaction_history(account):
                print(transaction)
            print("\nTotal Balance:" + str(account.get_balance()))
            print("**-----------------------------------------**")
        case '4':  # Transaction Statistics
            statistics = calculate_statistics(account.get_transactions())
            print("**-------** Transaction Statistics: **--------**")
            for key, value in statistics.items():
                print(f"{key}: {value}")
            print("**--------------------------------------------**")
        case '6':  # Exit
            exit()
        case _:
            print("Invalid choice")


# Generator for tracking transactions
def transaction_history(account):
    for trans in account.get_transactions():
        yield f"{trans['amount']:<10}   {trans['category']:<10}   {trans['date']:<25}   {trans['description']} "


# Calculate statistics for transactions
def calculate_statistics(transactions):
    amounts = [trans['amount'] for trans in transactions]
    Helper.create_plot(transactions)
    return {
        'total_transactions': len(transactions),
        'total_amount_transaction': sum(amounts),
    }


def main():
    while True:
        back = True
        while back:
            # Main signup menu
            option = signup_menu()
            back, accounts, user, is_admin = perform_signup(option)

        selected_account = accounts[-1]

        # Admin or Normal User Menu
        while True:
            if is_admin:
                choice = admin_menu()
                perform_admin_action(choice, user)
            else:
                choice = display_menu()
                if choice == '5':
                    del accounts
                    print("!!-----------Logged out Successfully------------!!")
                    break
                perform_action(choice, selected_account, AccountJSONManager(File.ACCOUNT.value))


if __name__ == "__main__":
    main()

