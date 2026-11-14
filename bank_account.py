class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount should be greater than 0.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount should be greater than 0.")
        elif self.balance < amount:
            raise InsufficientFundsError("Insufficient funds in account.")
        self.balance -= amount
        
    def __str__(self):
        return f"{self.owner}: ${self.balance}"


if __name__ == "__main__":
    gold_bank = BankAccount("James", 2000)
    print(gold_bank)
    try:
        amount_to_deposit = int(input("Enter amount to deposit: "))
        gold_bank.deposit(amount_to_deposit)
        print(gold_bank)
    except ValueError as e:
        print(e)
    try:
        amount_to_withdraw = int(input("Enter amount to be withdrawn: "))
        gold_bank.withdraw(amount_to_withdraw)
        print(gold_bank)
    except (ValueError, InsufficientFundsError) as e:
        print(e)       
