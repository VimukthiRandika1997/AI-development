import json

# ----------------------------
# Singleton: Logger
# ----------------------------

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class AppLogger(metaclass=SingletonMeta):
    def log(self, message):
        print(f"[LOG] {message}")

logger = AppLogger()


# ----------------------------
# Factory: Payment Methods
# ----------------------------

class Payment:
    def pay(self, amount): pass


class PayPal(Payment):
    def pay(self, amount):
        logger.log(f"Paid {amount} via PayPal")
        return f"Paid {amount} via PayPal"


class Stripe(Payment):
    def pay(self, amount):
        logger.log(f"Paid {amount} via Stripe")
        return f"Paid {amount} via Stripe"


class PaymentFactory:
    @staticmethod
    def get_payment(method):
        if method == "paypal":
            return PayPal()
        elif method == "stripe":
            return Stripe()
        else:
            return ValueError("Unknown payment method")


# ----------------------------
# Adapter: Legacy User System
# ----------------------------
        
class LegacyUserSystem:
    def get_user_data(self):
        return {"name": "Alice", "role": "user", "email": "alice@example.com"}

class UserAdapter:
    def __init__(self, legacy_user):
        self.legacy_user = legacy_user

    def get_user_json(self):
        return json.dumps(self.legacy_user.get_user_data())
    

# ----------------------------
# Decorator: Role-Based Access
# ----------------------------

def admin_required(func):
    def wrapper(user, *args, **kwargs):
        if user.get("role") != "admin":
            return "Access denied!"
        return func(user, *args, **kwargs)
    return wrapper


# ----------------------------
# Observer: Stock Notifications
# ----------------------------

class Stock:
    def __init__(self):
        self.observers = []
        self.items = {}

    def add_item(self, name, quantity):
        self.items[name] = quantity
        logger.log(f"Added {name} with quantity {quantity}")

    def attach(self, observer):
        self.observers.append(observer)

    def update_stock(self, name, quantity):
        if name in self.items:
            self.items[name] += quantity
            self.notify(name)

    def notify(self, name):
        for observer in self.observers:
            observer.update(name, self.items[name])

class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, item_name, quantity):
        print(f"{self.name} notified: {item_name} stock is now {quantity}")


# ----------------------------
# Strategy: Discount
# ----------------------------

class DiscountStrategy:
    def apply_discount(self, amount): return amount


class NoDiscount(DiscountStrategy):
    def apply_discount(self, amount): return amount


class TenPercentDiscount(DiscountStrategy):
    def apply_discount(self, amount): return amount * 0.9


class ShoppingCart:
    def __init__(self, discount_strategy: DiscountStrategy):
        self.items = {}
        self.strategy = discount_strategy

    def add_item(self, item_name, price, quantity=1):
        self.items[item_name] = {"price": price, "quantity": quantity}

    def checkout(self, payment_method: Payment):
        total = sum([v["price"] * v["quantity"] for v in self.items.values()])
        discounted_total = self.strategy.apply_discount(total)
        return payment_method.pay(discounted_total)


# ----------------------------
# E-commerce Simulation
# ----------------------------


# 1️⃣ Legacy user
legacy_user = LegacyUserSystem()
user = json.loads(UserAdapter(legacy_user).get_user_json())


# 2️⃣ Stock & Subscribers
stock = Stock()
stock.attach(Subscriber("Alice"))
stock.attach(Subscriber("Bob"))
stock.add_item("Laptop", 5)
stock.update_stock("Laptop", 3)  # Notifies subscribers


# 3️⃣ Admin-only action
@admin_required
def remove_item(user, stock, item_name):
    if item_name in stock.items:
        del stock.items[item_name]
        logger.log(f"{item_name} removed by {user['name']}")
        return f"{item_name} removed"
    return "Item not found"

print(remove_item(user, stock, "Laptop")) # Access denied!


# 4️⃣ Shopping Cart & Checkout
cart = ShoppingCart(TenPercentDiscount())
cart.add_item("Laptop", 1000, 1)
payment = PaymentFactory.get_payment("paypal")
print(cart.checkout(payment)) # Applies discount + payment



"""

| Pattern   | Where it is used                               |
| --------- | ---------------------------------------------- |
| Singleton | `AppLogger` logs everything                    |
| Factory   | `PaymentFactory` chooses payment method        |
| Adapter   | `UserAdapter` converts legacy user data        |
| Decorator | `admin_required` protects admin actions        |
| Observer  | `Stock` notifies `Subscribers` on stock change |
| Strategy  | `ShoppingCart` applies different discounts     |


"""