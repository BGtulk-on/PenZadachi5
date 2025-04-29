import abc
from functools import wraps

class DeliveryItem(abc.ABC):
    def __init__(self, sender: str, recipient: str):
        self.sender = sender
        self.recipient = recipient

    @abc.abstractmethod
    def get_details(self) -> str:
        pass

    def deliver(self):
        print(f"Delivering item from {self.sender} to {self.recipient}.")

def track_delivery(func):
    @wraps(func)
    def wrapper(item: DeliveryItem, *args, **kwargs):
        print(f"Tracking: Preparing delivery for item to {item.recipient}.")
        result = func(item, *args, **kwargs)
        print(f"Tracking: Delivery to {item.recipient} completed.")
        return result
    return wrapper

DeliveryItem.deliver = track_delivery(DeliveryItem.deliver)

class Letter(DeliveryItem):
    def __init__(self, sender: str, recipient: str, content: str):
        super().__init__(sender, recipient)
        self.content = content

    def get_details(self) -> str:
        return f"Letter from {self.sender} to {self.recipient}. Content: {self.content[:20]}..."

class Package(DeliveryItem):
    def __init__(self, sender: str, recipient: str, weight: float):
        super().__init__(sender, recipient)
        self.weight = weight

    def get_details(self) -> str:
        return f"Package from {self.sender} to {self.recipient}. Weight: {self.weight} kg."

class DeliveryCollection:
    def __init__(self, items: list[DeliveryItem]):
        self._items = items

    def __iter__(self):
        return iter(self._items)

def filter_heavy_packages(deliveries: DeliveryCollection):
    for item in deliveries:
        if isinstance(item, Package) and item.weight > 5:
            yield item

if __name__ == "__main__":
    letter1 = Letter("Алиса", "Боби", "Поверителна информация вътре.")
    package1 = Package("Чарли", "Давид", 3.5)
    package2 = Package("Ева", "Франк", 7.2)
    package3 = Package("Грейс", "Хайди", 6.0)

    all_deliveries = DeliveryCollection([letter1, package1, package2, package3])

    print("--- All Deliveries ---")
    for item in all_deliveries:
        print(item.get_details())
        item.deliver()
        print("-" * 10)

    print("\n--- Heavy Packages (over 5 kg) ---")
    heavy_packages_gen = filter_heavy_packages(all_deliveries)
    for heavy_package in heavy_packages_gen:
        print(heavy_package.get_details())
        heavy_package.deliver()
        print("-" * 10)
