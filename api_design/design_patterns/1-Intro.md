# Basic Design Patterns

Design patterns are standard solutions to common software design problems.

| Pattern   | Purpose         | Example Use Case  |
| --------- | --------------- | ----------------- |
| Singleton | One instance    | DB connection     |
| Factory   | Create objects  | UI widgets        |
| Adapter   | Bridge APIs     | Legacy code       |
| Decorator | Add behavior    | Logging, security |
| Observer  | Event handling  | Notifications     |
| Strategy  | Swap algorithms | Payment methods   |


## 🌟 Creational Patterns

These deal with object creation

### 1. Singleton Pattern

- Ensures only one instance of a class exists.

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def connect(self):
        return "Database connection established."

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True

```

✅ Use-cases:

- Database connections
- Logging system
- Config manager


### 2. Factory Pattern

- Creates objects without exposing creation logic

```python
class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        return "Drawing Circle"

class Square(Shape):
    def draw(self):
        return "Drawing Square"

class ShapeFactory:
    @staticmethod
    def get_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            return None

# Usage
shape = ShapeFactory.get_shape("circle")
print(shape.draw())
```

✅ Use-cases:

- UI components (buttons, text fields, etc.)
- Game objects (weapons, enemies)
- Machine learning models (different algorithms)


## 🌟 Structural Patterns

These deals with **class and object compositions**

### 3. Adapter Pattern

- Make incompatible interfaces work together.

```python
class OldPrinter:
    def old_print(self, text):
        return f"Old Printer: {text}"

class NewPrinter:
    def new_print(self, text):
        return f"New Printer: {text}"

class PrinterAdapter:
    def __init__(self, old_printer):
        self.old_printer = old_printer

    def new_print(self, text):
        return self.old_printer.old_print(text)

# Usage
old = OldPrinter()
adapter = PrinterAdapter(old)
print(adapter.new_print("Hello"))
```

✅ Use-cases:

- Integrating legacy code with new APIs
- Connecting third-party libraries
- Converting data formats


### 4. Decorator Pattern

- Adds functionality dynamically without modifying the original class.

```python
def bold_decorator(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def italic_decorator(func):
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper

@bold_decorator
@italic_decorator
def greet():
    return "Hello"

print(greet())  # <b><i>Hello</i></b>
```

✅ Use-cases:

- Logging, authentication in web apps
- Adding filters in image processing
- Adding formatting in GUIs


## 🌟 Behavioral Patterns

These deal with communication between objects.

### 5. Observer Pattern

- Notifies subscribers when an event happens

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def update(self, message):
        print(f"Received: {message}")

# Usage
subject = Subject()
observer1 = Observer()
observer2 = Observer()
subject.attach(observer1)
subject.attach(observer2)

subject.notify("New blog post published!")
```

✅ Use-cases:

- Event-driven systems (GUIs, messaging apps)
- Real-time notifications
- Stock market trackers


### 6. Strategy Pattern

- Defines a family of algorithms and makes them interchangeable

```python
class Strategy:
    def execute(self, a, b):
        pass

class Add(Strategy):
    def execute(self, a, b):
        return a + b

class Multiply(Strategy):
    def execute(self, a, b):
        return a * b

class Calculator:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def calculate(self, a, b):
        return self.strategy.execute(a, b)

# Usage
calc = Calculator(Add())
print(calc.calculate(3, 5))  # 8

calc = Calculator(Multiply())
print(calc.calculate(3, 5))  # 15
```

✅ Use-cases:

- Payment methods (PayPal, Stripe, Bank Transfer)
- Compression algorithms (zip, gzip, bzip2)
- Sorting strategies