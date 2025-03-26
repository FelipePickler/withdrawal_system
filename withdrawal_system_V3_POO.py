import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Customer:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class Individual(Customer):
    def __init__(self, name, birth_date, ssn, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.ssn = ssn

class Account:
    def __init__(self, number, customer):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._customer = customer
        self._history = History()

    @classmethod
    def new_account(cls, number, customer):
        return cls(number, customer)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def number(self):
        return self._number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def history(self):
        return self._history
    
    def withdraw(self, amount):
        balance = self._balance
        insufficient_funds = balance < amount

        if insufficient_funds:
            print("\n@@@ Operation failed! Insufficient funds! @@@")
        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True
        else:
            print("\n@@@ Operation failed! Invalid amount! @@@")
            return False
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
        else:
            print("\n@@@ Operation failed! Invalid amount! @@@")
            return False
        
        return True
    
class CheckingAccount(Account):
    def __init__(self, number, customer, limit=100000, withdrawal_limit=3):
        super().__init__(number, customer)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        num_withdrawals = len(
            [transaction for transaction in self.history.transactions
            if transaction["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdrawals = num_withdrawals >= self._withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! Amount exceeds the limit! @@@")
        elif exceeded_withdrawals:
            print("\n@@@ Operation failed! Withdrawal limit exceeded! @@@")
        else:
            return super().withdraw(amount)
        
        return False
    
    def __str__(self):
        return textwrap.dedent(f"""
            Agency: {self.agency}
            Account: {self.number}
            Holder: {self.customer.name}
        """)

class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def register(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount
    
    def register(self, account):
        successful_transaction = account.withdraw(self.amount)
        if successful_transaction:
            account.history.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount
    
    def register(self, account):
        successful_transaction = account.deposit(self.amount)
        if successful_transaction:
            account.history.add_transaction(self)

# Menu and other functions

def menu():
    menu_text = """
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [nc]\tNew account
    [lc]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu_text))

def filter_customer(ssn, customers):
    filtered_customers = [customer for customer in customers if customer.ssn == ssn]
    return filtered_customers[0] if filtered_customers else None

def retrieve_customer_account(customer):
    if not customer.accounts:
        print("\n@@@ Customer does not have an account! @@@")
        return
    return customer.accounts[0]

def deposit(customers):
    ssn = input("Enter customer SSN: ")
    customer = filter_customer(ssn, customers)
    if not customer:
        print("\n@@@ Customer not found! @@@")
        return
    amount = float(input("Enter deposit amount: "))
    transaction = Deposit(amount)
    account = retrieve_customer_account(customer)
    if not account:
        return
    customer.perform_transaction(account, transaction)

def withdraw(customers):
    ssn = input("Enter customer SSN: ")
    customer = filter_customer(ssn, customers)
    if not customer:
        print("\n@@@ Customer not found! @@@")
        return
    amount = float(input("Enter withdrawal amount: "))
    transaction = Withdrawal(amount)
    account = retrieve_customer_account(customer)
    if not account:
        return
    customer.perform_transaction(account, transaction)

def display_statement(customers):
    ssn = input("Enter customer SSN: ")
    customer = filter_customer(ssn, customers)
    if not customer:
        print("\n@@@ Customer not found! @@@") 
        return
    account = retrieve_customer_account(customer)
    if not account:
        return
    
    print("\n================ Statement ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions were made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\tR$ {transaction['amount']:.2f}"

    print(statement)
    print(f"\nBalance:\n\tR$ {account.balance:.2f}")
    print("=========================================")

def create_customer(customers):
    ssn = input("Enter SSN (numbers only): ")
    customer = filter_customer(ssn, customers)

    if customer:
        print("\n@@@ A customer with this SSN already exists! @@@")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state abbreviation): ")

    customer = Individual(name=name, birth_date=birth_date, address=address, ssn=ssn)

    customers.append(customer)

    print("=== User created successfully! ===")

def create_account(account_number, customers, accounts):
    ssn = input("Enter customer SSN: ")
    customer = filter_customer(ssn, customers)

    if not customer:
        print("\n@@@ Customer not found, account creation aborted! @@@")
        return
    
    account = CheckingAccount.new_account(customer=customer, number=account_number)
    accounts.append(account)
    customer.add_account(account)

    print("\n=== Account created successfully! ===")

def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))
        
def main():
    customers = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            deposit(customers)

        elif option == "w":
            withdraw(customers)

        elif option == "s":
            display_statement(customers)

        elif option == "nu":
            create_customer(customers)

        elif option == "nc":
            account_number = len(accounts) + 1
            create_account(account_number, customers, accounts) 

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\n@@@ Invalid operation, please select again. @@@")

main()
