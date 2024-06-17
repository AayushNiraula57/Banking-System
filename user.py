import json
import random
from datetime import datetime, timedelta
from helper import Helper
from send_email import Email


# User class
class User:
    def __init__(self, email, password,  username=None, role=None):
        self.__email = email
        self.__username = username
        self.__password = password
        self.__account_number = random.randint(1000, 10000000)
        self.__role = role
        self.__otp = None
        self.__otp_expiry = None

    def create_user(self, filename):
        with open(filename, 'r+') as file:
            first_char = file.read(1)
            if not first_char:
                file_data = {}
            else:
                file.seek(0)
                file_data = json.load(file)
            file_data.update(self.__dict__())
            file.seek(0)
            json.dump(file_data, file, indent=4, separators=(', ', ': '))
        print("Your account number is: " + str(self.__account_number) + '\n')
        return self.__account_number

    def user_exists(self, filename):
        # Helper.check_if_file_exists(filename)
        exists = False
        invalid_pass = False
        with open(filename, 'r') as file:
            first_char = file.read(1)
            if not first_char:
                result = (exists, invalid_pass)
                return result
            else:
                file.seek(0)
                data = json.load(file)
                for user_id, user_data in data.items():
                    if self.__email == user_data['email'] and self.__password == user_data['password']:
                        exists = True
                        self.__username = user_data['username']
                        self.__account_number = user_id
                        self.__role = user_data['role']
                        self.__otp = random.randint(1000, 9999)
                        self.__otp_expiry = datetime.now() + timedelta(minutes=1)
                        break
                    elif self.__email == user_data['email'] and self.__password != user_data['password']:
                        exists = True
                        invalid_pass = True
                        break
            result = (exists, invalid_pass)
        return result

    def login(self, filename):
        exists_user, invalid_pass = self.user_exists(filename)
        is_logged_in = False
        if not exists_user:
            print("!!------User Not Found-----!!")
        elif exists_user and invalid_pass:
            print("!!------Invalid Password-----!!")
        else:
            email = Email()
            body, subject = email.get_otp_email_content(self.__otp)
            success = email.send_email(body, subject, self.__email)
            if success:
                print("Otp sent successfully to your email!!")
            #print("Your otp is:", self.__otp)
            otp = input("Enter Otp: ")
            is_otp_valid = Helper.verify_otp(otp, self)
            if is_otp_valid:
                is_logged_in = True

        return is_logged_in, self

    def register(self, filename):
        exists_user, _ = self.user_exists(filename)
        account_number = None
        registered = False
        if not exists_user:
            self.__otp = random.randint(1000, 9999)
            self.__otp_expiry = datetime.now() + timedelta(minutes=1)
            account_number = self.create_user(filename)
            email = Email()
            body, subject = email.get_otp_email_content(self.__otp)
            success = email.send_email(body, subject, self.__email)
            if success:
                print("Otp sent successfully to your email!!")
            #print("Your otp is:", self.__otp)
            otp = input("Enter Otp: ")
            is_otp_valid = Helper.verify_otp(otp, self)
            if is_otp_valid:
                registered = True
                print("!-----------New Account Created---------------!")
        else:
            print("User with the email already exists")

        return registered, self

    def get_role(self):
        return self.__role

    def get_otp(self):
        return self.__otp

    def get_otp_expiry(self):
        return self.__otp_expiry

    def get_email(self):
        return self.__email

    def get_details(self):
        return self.__email, self.__username, self.__account_number

    def __dict__(self):
        data = {
            self.__account_number: {
                "email": self.__email,
                "username": self.__username,
                "password": self.__password,
                "role": self.__role
            }}
        return data


class NormalUser(User):
    def __init__(self, email, password, username=None):
        super().__init__(email, password,  username, 'Normal')


class AdminUser(User):
    def __init__(self, email, password, username=None):
        super().__init__(email, password,  username, 'Admin')

    @staticmethod
    def delete_user(acc_number, filename):
        is_empty = Helper.check_file_exists_or_empty(filename)
        if not is_empty:
            try:
                with open(filename, 'r') as file:
                    data = file.read()
                    users = json.loads(data)
                    if acc_number in users:
                        removed_user = users.pop(acc_number)
                        print(f"Removed User: {removed_user}")
                        with open(filename, 'w') as file:
                            # Update values of existing keys
                            for key, value in users.items():
                                users[str(key)] = value
                            file.seek(0)
                            json.dump(users, file, indent=4, separators=(', ', ': '))
                    else:
                        print("User not found.")
            except Exception as e:
                print(e)

    @staticmethod
    def view_users(filename):
        with open(filename, 'r') as file:
            first_char = file.read(1)
            if not first_char:
                print("No users found!!!")
            else:
                file.seek(0)
                data = json.load(file)
                counter = 0
                print(f"Index \t\t  Name \t\t\t Email \t\t\t Account Number")
                for user_id, user_data in data.items():
                    counter += 1
                    print(f"{counter:<10} {user_data['username']:<25} {user_data['email']:<30} {user_id:<10}")
