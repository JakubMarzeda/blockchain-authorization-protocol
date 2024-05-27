import hashlib
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()

class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.balance = 0

    def deposit_funds(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.users = {}

    def create_genesis_block(self):
        return Block(0, datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def add_user(self, login, password):
        if login not in self.users:
            self.users[login] = User(login, password)

    def authorize_transaction(self, sender, receiver, amount):
        if sender in self.users and receiver in self.users:
            sender_user = self.users[sender]
            receiver_user = self.users[receiver]

            if sender_user.balance >= amount:
                sender_user.balance -= amount
                receiver_user.balance += amount

                transaction_data = {"sender": sender, "receiver": receiver, "amount": amount}
                transaction = Transaction(transaction_data)
                new_block = Block(len(self.chain), datetime.now(), transaction, self.get_latest_block().hash)
                new_block.hash = new_block.calculate_hash()
                self.chain.append(new_block)
                return True
            else:
                return False
        else:
            return False

    def authenticate_user(self, login, password):
        if login in self.users:
            user = self.users[login]
            if user.password == password:
                return True
        return False
    
    def display_chain(self):
        for block in self.chain:
            print(f"Block {block.index}")
            print(f"Timestamp: {block.timestamp}")
            if isinstance(block.data, Transaction):
                transaction_data = block.data.transaction_data
                print(f"Transaction: Sender - {transaction_data['sender']}, Receiver - {transaction_data['receiver']}, Amount - {transaction_data['amount']}")
            else:
                print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print("------------------")
    
    def display_users(self):
        for login, user in self.users.items():
            print(f"User: {login}, Balance: {user.balance}")

class Transaction:
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data
        self.timestamp = datetime.now()


blockchain = Blockchain()

while True:
    print("\nBlockchain Operations:")
    print("1. Add User")
    print("2. Authorize Transaction")
    print("3. Deposit Funds")
    print("4. Display Blockchain")
    print("5. Display Users")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        login = input("Enter login: ")
        password = input("Enter password: ")
        blockchain.add_user(login, password)
        print("User added successfully!")

    elif choice == "2":
        sender = input("Enter sender login: ")
        receiver = input("Enter receiver login: ")
        amount = float(input("Enter amount to transfer: "))
        if blockchain.authorize_transaction(sender, receiver, amount):
            print("Transaction authorized and added to the blockchain.")
        else:
            print("Transaction authorization failed. Check user's login or insufficient balance.")

    elif choice == "3":
        user_id = input("Enter login: ")
        amount = float(input("Enter amount to deposit: "))
        if user_id in blockchain.users:
            user = blockchain.users[user_id]
            if user.deposit_funds(amount):
                print(f"Funds deposited successfully. New balance: {user.balance}")
            else:
                print("Invalid amount. Deposit failed.")
        else:
            print("User not found.")

    elif choice == "4":
        print("\nCurrent Blockchain:")
        blockchain.display_chain()
    
    elif choice == "5":
        print("\nUsers:")
        blockchain.display_users()

    elif choice == "6":
        print("Exiting Blockchain Application.")
        break

    else:
        print("Invalid choice. Please choose again.")