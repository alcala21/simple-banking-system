# Write your code here
import random
import sqlite3


class CCSystem:

    def __init__(self):
        self.IIN = "400000"
        self.account = None
        self.pin = None
        self.balance = 0
        self.db_file = "card.s3db"
        self.conn = None
        self.cur = None
        self.connect_database()

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
        self.pin = f"{int(10000 * random.random()):04d}"
        self.save_card()
        message = "\n".join(["Your card has been created",
                            "Your card number:",
                            self.account,
                            "Your card PIN:",
                            self.pin])
        self.print_message(message)

    def log_into_account(self):
        account = input("Enter your card number: \n>")
        pin = input("Enter your PIN: \n>")

        if self.is_valid_account(account, pin):
            self.print_message("You have successfully logged in!")
            return self.show_balance(account)
        else:
            self.print_message("Wrong card number or PIN!")
        return True

    def generate_number(self):
        last_account = self.get_last_account()
        cardnum = f"{int(last_account[10:15]) + 1:05d}"
        temp_account = last_account[:10] + cardnum
        last_digit = self.get_last_digit(temp_account)
        temp_account += last_digit
        self.account = temp_account


    def get_last_digit(self, _account):
        digits = [x - 9 if x > 9 else x for x in
                  [2 * int(_account[i]) if i % 2 == 0 else int(_account[i])
                   for i in range(len(_account))]]
        return str((10 - (sum(digits) % 10)) % 10)

    def show_balance(self, account):
        while True:
            selection = int(input("1. Balance \n2. Log out \n0. Exit\n> "))
            if selection == 1:
                self.print_message(f"Balance: {self.balance}")
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

    def connect_database(self):
        self.conn = sqlite3.connect(self.db_file)

        if self.conn:
            self.cur = self.conn.cursor()

            create_table_if_not_there = """CREATE TABLE IF NOT EXISTS card (
                            id integer PRIMARY KEY,
                            number text,
                            pin text,
                            balance integer default 0);"""
            self.cur.execute(create_table_if_not_there)

    def get_last_account(self):
        query = "select count(*) from card;"
        self.cur.execute(query)

        if self.cur.fetchone()[0] > 0:
            query = "select number from card order by id desc limit 1;"
            self.cur.execute(query)
            last_account = self.cur.fetchone()[0]
        else:
            last_account = self.IIN + "100000000"

        return last_account

    def save_card(self):
        query = """insert into card(number, pin) values (?, ?)"""
        self.cur.execute(query, (self.account, self.pin))
        self.conn.commit()
        return self.cur.lastrowid

    def is_valid_account(self, _account, _pin):
        query = """select balance from card where number = ? and pin = ?;"""
        self.cur.execute(query, (_account, _pin))
        account_info = self.cur.fetchone()
        if not account_info:
            return False
        else:
            self.account = _account
            self.pin = _pin
            self.balance = account_info[0]
            return True


mycard = CCSystem()

while mycard.start():
    pass

