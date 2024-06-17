from transactions import Transaction
from abc import ABC,abstractmethod


class Bank(ABC):

    @abstractmethod
    def deposit(self, amount, description, account_manager):
        pass

    @abstractmethod
    def withdraw(self, amount, description, account_manager):
        pass

    @abstractmethod
    def get_balance(self):
        pass


class Account(Bank):
    def __init__(self, name, account_number, balance=None, transactions=None):
        self.name = name
        self._balance = 0 if balance is None else balance
        self._transactions = [] if transactions is None else transactions
        self._account_number = account_number
        self.obj_transaction = None

    def deposit(self, amount, description, account_manager):
        self._balance += amount
        self.obj_transaction = Transaction(amount, description, category="Deposit")
        self._transactions.append(self.obj_transaction.__dict__())
        account_data = self.__dict__()
        account_manager.save_accounts(account_data)
        print(f'{amount} deposited successfully.')

    def withdraw(self, amount, description, account_manager):
        if self._balance >= amount:
            self._balance -= amount
            self.obj_transaction = Transaction(amount, description, category="Withdraw")
            self._transactions.append(self.obj_transaction.__dict__())
            account_data = self.__dict__()
            account_manager.save_accounts(account_data)
            print(f'{amount} withdrawn successfully.')
        else:
            print("Insufficient Balance!!!")
            print(f"Remaining Balance: {self._balance}")

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def get_transactions(self):
        return self._transactions

    def __dict__(self):
        data = {
            self._account_number: {
                "name": self.name,
                "balance": self._balance,
                "transactions": self._transactions
                #"account_number": self._account_number

            }
        }
        return data

