from datetime import datetime


class Transaction:
    def __init__(self,amount, description, category=None):
        self.amount = amount
        self.description = description
        self.category = category
        self.trans_date = datetime.now().strftime("%d %b, %Y  %I:%M:%S %p")

    def __dict__(self):
        data = {
                    "amount": self.amount,
                    "description": self.description,
                    "category": self.category,
                    "date": self.trans_date
                }
        return data
