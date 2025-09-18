# MVC Pattern

This patterns separates data in GUIs from the ways it is presented and accepted.

```python
from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def get(self, item):
        """Returns an object with a .items() call method
        that iterate over key, value pairs of its information.
        """
        pass

    @property
    @abstractmethod
    def item_type(self):
        pass

class View(ABC):
    @abstractmethod
    def show_item_list(self, item_type, item_list):
        pass

    @abstractmethod
    def show_item_information(self, item_type, item_name, item_info):
        """Will look for item information by iterating over key, value pairs
        yeilded by item_info.items()
        """
        pass
    
    @abstractmethod
    def item_not_found(self, item_type, item_name):
        pass


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = list(self.model)
        item_type = self.model.item_type
        self.view.show_item_list(item_type, items)

    def show_item_information(self, item_name):
        """
        Show information about a {item_type} item.
        :param str item_name: the name of the {item_type} item ot show information about
        """

        try:
            item_info = self.model.get(item_name)
        except Exception:
            item_type = self.model.item_type
            self.view.item_not_found(item_type, item_name)
        else:
            item_type = self.model.item_type
            self.view.show_item_information(item_type, item_name, item_info)
```