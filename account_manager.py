from account import Account
from helper import Helper
import json
import os


class AccountJSONManager:
    def __init__(self, filename):
        self.filename = filename

    def save_accounts(self, account_info):
        with open(self.filename, 'r+') as file:
            content = file.read()
            if self.check_file_is_empty():
                file_data = {}
            else:
                file.seek(0)
                file_data = json.loads(content)

        with open(self.filename, 'w') as file:
            # Update values of existing keys
            for key, value in account_info.items():
                file_data[str(key)] = value
            file.seek(0)
            json.dump(file_data,file, indent=4, separators=(', ', ': '))

    def load_accounts(self):
        # Load user account from file
        try:
            if not self.check_file_is_empty():
                with open(self.filename, 'r') as file:
                    json_data = file.read().strip()
                    data = json.loads(json_data)
                    accounts = []
                    for acc_num,acc_data in data.items():
                        account = Account(name=acc_data['name'],account_number=acc_num)
                        account._balance = acc_data['balance']
                        account._transactions = acc_data['transactions']
                        accounts.append(account)
                    return accounts
            else:
                accounts = []
                return accounts
        except FileNotFoundError:
            return []

    def check_file_is_empty(self):
        check_file = os.path.getsize(self.filename)
        if check_file == 0:
            return True
        else:
            return False
