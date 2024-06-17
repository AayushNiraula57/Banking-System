import os
import re
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from matplotlib.dates import DateFormatter, AutoDateLocator


class NegativeValueException(Exception):
    """Invalid amount"""
    pass


class MinimumAmountException(Exception):
    """Minimum amount 500"""
    pass


class MultipleOfHundredException(Exception):
    """Amount Multiple of Hundred"""
    pass


class Helper:
    @staticmethod
    def is_amount_valid(amount):
        try:
            amount = float(amount)
            if amount < 0:
                raise NegativeValueException
            elif amount<500:
                raise MinimumAmountException
            elif amount%10 != 0:
                raise MultipleOfHundredException
        except ValueError:
            print('!!----Amount Must be in numbers----!!')
            return False
        except NegativeValueException as e:
            print("!!----Amount cannot be negative----!!")
            return False
        except MinimumAmountException as e:
            print("!!----Minimum amount must be 500----!!")
            return False
        except MultipleOfHundredException as e:
            print("!!----Amount must be multiple of 100----!!")
            return False
        return True

    @staticmethod
    def check_if_file_exists(filename):
        # Check if file exists
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass

    @staticmethod
    def check_email(account_email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, account_email):
            return True
        else:
            print("Invalid email address")
            return False

    @staticmethod
    def check_name(account_name):
        name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*(?: [a-zA-Z]+)?$'
        if re.match(name_pattern, account_name):
            return True
        else:
            print("Invalid Name")
            return False

    @staticmethod
    def check_password(password):
        password_pattern = r'[\w\s\S]{4,}'
        if re.match(password_pattern, password):
            return True
        else:
            print("Invalid Password")
            print("Passport must be at least 4 digits")
            return False

    @staticmethod
    def verify_otp(otp, user):
        if datetime.now() > user.get_otp_expiry():
            print("Otp expired !!!")
            return False

        if int(otp) == user.get_otp():
            return True
        else:
            print("Otp invalid !!!")
            return False

    @staticmethod
    def create_plot(transactions):
        # Extract deposit and withdrawal transactions
        amount_data = defaultdict(float)
        amount = 0
        for transaction in transactions:
            date = datetime.strptime(transaction['date'], '%d %b, %Y  %I:%M:%S %p')
            category = transaction['category']
            if category == 'Deposit':
                amount += transaction['amount']
                amount_data[date] = amount
            elif category == 'Withdraw':
                amount -= transaction['amount']
                amount_data[date] = amount
        # Sort the data by date
        amount_data = dict(sorted(amount_data.items()))
        # Plotting
        plt.figure(figsize=(14, 6))

        plt.plot(list(amount_data.keys()), list(amount_data.values()), label='Transactions', marker='o', color='red')

        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Deposit and Withdrawal Transactions Over Time')
        plt.legend()

        date_fmt = DateFormatter('%m-%d %H:%M')  # Format for date and time
        plt.gca().xaxis.set_major_formatter(date_fmt)  # Set the date and time format
        plt.gca().xaxis.set_major_locator(AutoDateLocator())  # Automatically adjust the date and time ticks

        plt.grid(True)
        plt.tight_layout()

        plt.show()

        return

    @staticmethod
    def check_file_exists_or_empty(filename):

        file = os.path.exists(filename)
        if not file:
            print("File does not exists")
            return True
        file_size = os.path.getsize(filename)
        if file_size == 0:
            print("File is empty")
            return True
        else:
            return False
