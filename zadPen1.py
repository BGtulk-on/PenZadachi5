from abc import ABC, abstractmethod
import functools

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"LOG: Preparing {args[0].__class__.__name__}...")
        return func(*args, **kwargs)
    return wrapper

class MenuItem(ABC):
    @abstractmethod
    def price(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

class Pizza(MenuItem):
    def price(self):
        return 15.99

    @log_action
    def prepare(self):
        print("Preparing Pizza.")

class Salad(MenuItem):
    def price(self):
        return 8.50

    @log_action
    def prepare(self):
        print("Preparing Salad.")

class OrderIterator:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._items):
            result = self._items[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

if __name__ == "__main__":
    order_items = [Pizza(), Salad(), Pizza()]
    order_iterator = OrderIterator(order_items)

    print("Processing order:")
    total_price = 0
    for item in order_iterator:
        item.prepare()
        total_price += item.price()
        print(f"Item price: ${item.price():.2f}")
        print("-" * 20)

    print(f"Total order price: ${total_price:.2f}")
