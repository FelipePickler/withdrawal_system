import textwrap

def menu():
    menu_text = """\n
    =============== MENU ===============

    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [nc]\tNew account
    [la]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu_text))


def deposit(balance, amount, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Deposit:\t$ {amount:.2f}\n"
        print("\n=== Deposit completed successfully! ===")
    else:
        print("\n@@@ Operation failed! The amount entered is invalid. @@@")

    return balance, statement


def withdraw(*, balance, amount, statement, limit, withdrawals_count, withdrawals_limit):
    exceeded_balance = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdrawals = withdrawals_count >= withdrawals_limit

    if exceeded_balance:
        print("\n@@@ Operation failed! You do not have sufficient balance. @@@")

    elif exceeded_limit:
        print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")

    elif exceeded_withdrawals:
        print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal:\t$ {amount:.2f}\n"
        withdrawals_count += 1
        print("\n=== Withdrawal completed successfully! ===")

    else:
        print("\n@@@ Operation failed! The amount entered is invalid. @@@")

    return balance, statement, withdrawals_count


def display_statement(balance, /, *, statement):
    print("\n================ STATEMENT ================")
    print("No transactions have been made." if not statement else statement)
    print(f"\nBalance:\t\t$ {balance:.2f}")
    print("===========================================")


def create_user(users):
    cpf = input("Enter the user's CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\n@@@ User already registered. @@@")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter date of birth (dd-mm-yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state abbreviation): ")

    users.append({"name": name, "cpf": cpf, "birth_date": birth_date, "address": address})
    print("=== User registered successfully! ===")


def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def create_account(agency, account_number, users):
    cpf = input("Enter the user's CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\n=== Account created successfully! ===")
        return {"agency": agency, "account_number": account_number, "user": user}
    
    print("\n@@@ User not found, account creation process terminated! @@@")

    
def list_accounts(accounts):
    for account in accounts:
        line = f"""\  
            Agency:\t{account["agency"]}
            Account:\t{account["account_number"]}
            Holder:\t{account["user"]["name"]}
    """
    print("=" * 100)
    print(textwrap.dedent(line))


def main():
    WITHDRAWALS_LIMIT = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    statement = ""
    withdrawals_count = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            amount = float(input("Enter the deposit amount: "))

            balance, statement = deposit(balance, amount, statement)

        elif option == "w":
            amount = float(input("Enter the withdrawal amount: "))

            balance, statement, withdrawals_count = withdraw(
                balance=balance,
                amount=amount,
                statement=statement,
                limit=limit,
                withdrawals_count=withdrawals_count,
                withdrawals_limit=WITHDRAWALS_LIMIT,
            )

        elif option == "s":
            display_statement(balance, statement=statement)

        elif option == "nu":
            create_user(users)

        elif option == "nc":
            account_number = len(accounts) + 1
            account = create_account(AGENCY, account_number, users)

            if account:
                accounts.append(account)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            print("\n=== Thank you for using our banking system! ===")
            break
        
        else:
            print("Invalid operation, please select a valid option again.")


main()
