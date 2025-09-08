# Basic Design Patterns: Examples

These are just examples for the learning purpose.

| Pattern   | Real-World Example                |
| --------- | --------------------------------- |
| Singleton | One global logger                 |
| Factory   | Payment gateways (PayPal, Stripe) |
| Adapter   | Legacy system to JSON             |
| Decorator | Role-based access control         |
| Observer  | Stock price notifications         |
| Strategy  | Discount strategies               |


## 1. Singleton → Logging System

```python
class Logger(metaclass=type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class AppLogger(metaclass=Logger):
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)
        print(f"[LOG] {message}")

# Usage
logger1 = AppLogger()
logger2 = AppLogger()
logger1.log("Application started")
logger2.log("User logged in")

print(logger1 is logger2)  # True
```


✅ Use-case: Only one global logger instance.


## 2. Factory → Payment Gateway Factory

```python
class Payment:
    def pay(self, amount): pass

class PayPal(Payment):
    def pay(self, amount):
        return f"Paid {amount} via PayPal"

class Stripe(Payment):
    def pay(self, amount):
        return f"Paid {amount} via Stripe"

class PaymentFactory:
    @staticmethod
    def get_payment(method):
        if method == "paypal":
            return PayPal()
        elif method == "stripe":
            return Stripe()
        else:
            raise ValueError("Unknown payment method")

# Usage
payment = PaymentFactory.get_payment("paypal")
print(payment.pay(100))
```

✅ Use-case: Easily add new payment methods without changing core code.


## 3. Adapter → Legacy Data to JSON

```python
import json

class LegacySystem:
    def get_data(self):
        return {"user": "Alice", "age": 30}

class JSONAdapter:
    def __init__(self, legacy_system):
        self.legacy_system = legacy_system

    def get_json(self):
        return json.dumps(self.legacy_system.get_data())

# Usage
legacy = LegacySystem()
adapter = JSONAdapter(legacy)
print(adapter.get_json())
```

✅ Use-case: Integrating legacy data format with modern JSON-based APIs.


## 4. Decorator → Role-Based Access Control

```python
def admin_required(func):
    def wrapper(user, *args, **kwargs):
        if user != "admin":
            return "Access denied!"
        return func(user, *args, **kwargs)
    return wrapper

@admin_required
def delete_user(user, username):
    return f"{username} deleted by {user}"

# Usage
print(delete_user("guest", "Alice"))  # Access denied!
print(delete_user("admin", "Alice"))  # Alice deleted by admin

```

✅ Use-case: Security checks in web apps.


## 5. Observer → Stock Price Notifier

```python
class Stock:
    def __init__(self):
        self.observers = []
        self.price = 0

    def attach(self, observer):
        self.observers.append(observer)

    def set_price(self, price):
        self.price = price
        self.notify()

    def notify(self):
        for observer in self.observers:
            observer.update(self.price)

class Investor:
    def __init__(self, name):
        self.name = name

    def update(self, price):
        print(f"{self.name} notified: Stock price is {price}")

# Usage
stock = Stock()
stock.attach(Investor("Alice"))
stock.attach(Investor("Bob"))
stock.set_price(120)
```

✅ Use-case: Investors get notified of stock price changes.


## 6. Strategy → Discount Strategies in Shopping Cart

```python
class DiscountStrategy:
    def apply_discount(self, amount): return amount

class NoDiscount(DiscountStrategy):
    def apply_discount(self, amount): return amount

class PercentageDiscount(DiscountStrategy):
    def apply_discount(self, amount): return amount * 0.9  # 10% off

class FixedDiscount(DiscountStrategy):
    def apply_discount(self, amount): return amount - 20

class ShoppingCart:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def checkout(self, amount):
        return self.strategy.apply_discount(amount)

# Usage
cart = ShoppingCart(PercentageDiscount())
print("Final price:", cart.checkout(200))  # 180
```

✅ Use-case: Switch discounts without changing checkout code.