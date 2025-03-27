# Withdrawal System V3 (Object-Oriented Programming)

## Installation

To use this withdrawal system, you can simply download the `withdrawal_system_V3_POO.py` file and run it using a Python interpreter.

## Usage

The withdrawal system provides the following functionalities:

1. **Deposit**: Allows you to deposit money into a customer's account.
2. **Withdraw**: Allows you to withdraw money from a customer's account, subject to withdrawal limits.
3. **Statement**: Displays the transaction history and current balance for a customer's account.
4. **New Account**: Allows you to create a new account for a customer.
5. **New User**: Allows you to create a new customer.
6. **List Accounts**: Displays the details of all existing accounts.

To use the system, simply run the `main()` function in the `withdrawal_system_V3_POO.py` file. The program will present a menu with the available options.

## API

The main classes and their methods are:

1. `Customer`:
   - `perform_transaction(self, account, transaction)`: Performs a transaction on the customer's account.
   - `add_account(self, account)`: Adds an account to the customer's list of accounts.

2. `Account`:
   - `withdraw(self, amount)`: Withdraws the specified amount from the account, if sufficient funds are available.
   - `deposit(self, amount)`: Deposits the specified amount into the account.

3. `CheckingAccount` (inherits from `Account`):
   - `withdraw(self, amount)`: Withdraws the specified amount from the account, subject to withdrawal limits.

4. `History`:
   - `add_transaction(self, transaction)`: Adds a transaction to the account's transaction history.

5. `Transaction` (abstract base class):
   - `register(self, account)`: Registers the transaction with the specified account.

6. `Withdrawal` (implements `Transaction`):
   - `register(self, account)`: Registers a withdrawal transaction with the specified account.

7. `Deposit` (implements `Transaction`):
   - `register(self, account)`: Registers a deposit transaction with the specified account.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To test the withdrawal system, you can run the `main()` function and interact with the system through the provided menu options. You can create new customers, accounts, and perform various transactions to ensure the system is working as expected.