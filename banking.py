# Write your code here
import random


class CCSystem:

    def __init__(self):
        self.accounts = []
        self.account_info = {}
        self.IIN = "400000"
        self.last_account = "100000000"

    def start(self):
        selection = int(input("1. Create an account \n2. Log into account \n0. Exit\n> "))

        if selection == 1:
            self.generate_account()
        elif selection == 2:
            return self.log_into_account()
        elif selection == 0:
            return self.bye()

        return True

    def generate_account(self):
        self.generate_number()
        self.account_info[self.accounts[-1]] = self.pin_and_balance()
        message = "\n".join(["Your card has been created",
                "Your card number:",
                self.accounts[-1],
                "Your card PIN:",
                self.account_info[self.accounts[-1]]['pin']])
        self.print_message(message)

    def log_into_account(self):
        account = input("Enter your card number: \n>")
        pin = input("Enter your PIN: \n>")
        if account in self.account_info and pin == self.account_info[account]['pin']:
            self.print_message("You have successfully logged in!")
            return self.show_balance(account)
        else:
            self.print_message("Wrong card number or PIN!")

        return True

    def generate_number(self):
        account = str(int(self.last_account) + 1)
        last_digit = self.get_last_digit(account)
        self.accounts.append(self.IIN + account + str(last_digit))
        self.last_account = account

    def get_last_digit(self, account):
        loc_account = self.IIN + account
        digits = [x - 9 if x > 9 else x for x in
                  [2 * int(loc_account[i]) if i % 2 == 0 else int(loc_account[i])
                   for i in range(len(loc_account))]]
        return (10 - (sum(digits) % 10)) % 10

    def pin_and_balance(self):
        return {'pin': f"{int(10000 * random.random()):04d}", 'balance': 0}

    def show_balance(self, account):
        while True:
            selection = int(input("1. Balance \n2. Log out \n0. Exit\n> "))
            if selection == 1:
                self.print_message(f"Balance: {self.account_info[account]['balance']}")
            elif selection == 2:
                self.print_message("You have successfully logged out!")
                return True
            else:
                return self.bye()

    def bye(self):
        self.print_message("Bye!")
        return False

    def print_message(self, message):
        print()
        print(message)
        print()




mycard = CCSystem()

while mycard.start():
    pass

