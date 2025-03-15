class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.__balance = balance  # Private variable
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{amount} deposited successfully.")
        else:
            print("Invalid deposit amount.")
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"{amount} withdrawn successfully.")
        else:
            print("Insufficient funds or invalid amount.")
    
    def get_balance(self):
        return self.__balance

# Usage
# account = BankAccount("Aminat", 1000)
# account.deposit(500)
# print(account.get_balance())  # 1500
# print(account.__balance)  # This would raise an AttributeError
