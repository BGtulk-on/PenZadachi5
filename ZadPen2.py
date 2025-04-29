from abc import ABC, abstractmethod
import functools

def authorize(func):
    @functools.wraps(func)
    def wrapper(self, amount):
        print(f"Authorizing payment of {amount}...")
        print("Authorization successful.")
        return func(self, amount)
    return wrapper

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    @authorize
    def pay(self, amount):
        print(f"Paying {amount} using Credit Card ending with {self.card_number[-4:]}.")
        return {"method": "CreditCard", "amount": amount, "status": "Success"}

class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email

    @authorize
    def pay(self, amount):
        print(f"Paying {amount} using PayPal account {self.email}.")
        return {"method": "PayPal", "amount": amount, "status": "Success"}

class TransactionHistory:
    def __init__(self):
        self._transactions = []

    def add_transaction(self, transaction_details):
        if transaction_details and transaction_details.get("status") == "Success":
            self._transactions.append(transaction_details)
        else:
            print("Transaction failed or details missing, not adding to history.")


    def __iter__(self):
        return iter(self._transactions)

if __name__ == "__main__":
    cc = CreditCard("8932-5678-9012-0029")
    pp = PayPal("bgtulk123@gmail.com")
    history = TransactionHistory()

    print("--- Processing Payments ---")
    transaction1 = cc.pay(100)
    history.add_transaction(transaction1)

    print("-" * 20)
    transaction2 = pp.pay(50)
    history.add_transaction(transaction2)

    print("-" * 20)

    print("\n--- Transaction History ---")
    for tx in history:
        print(f"Method: {tx['method']}, Amount: {tx['amount']}, Status: {tx['status']}")