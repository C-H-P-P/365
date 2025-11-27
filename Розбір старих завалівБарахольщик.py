from dataclasses import dataclass, field
from datetime import datetime
import csv

@dataclass(order=True)
class Item:
   
    sort_index: tuple = field(init=False, repr=False)

    name: str
    category: str
    quantity: int
    value: float
    condition: str
    location: str
    added_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __post_init__(self):
     
        self.sort_index = (self.category.lower(), self.value)

    def total_value(self):
    
        return self.quantity * self.value

    def __str__(self):
   
        return (
            f"[{self.category}] {self.name} "
            f"({self.quantity} шт.) — {self.value} грн/шт, "
            f"стан: {self.condition}"
        )


@dataclass
class Inventory:
    items: list[Item] = field(default_factory=list)


    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, name: str):
       
        self.items = [i for i in self.items if i.name != name]

    def find_by_category(self, category: str):
    
        return [i for i in self.items if i.category.lower() == category.lower()]

    def total_inventory_value(self):
     
        return sum(i.total_value() for i in self.items)


    def save_to_csv(self, filename):
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "category", "quantity", "value", "condition", "location", "added_at"])
            for item in self.items:
                writer.writerow([
                    item.name, item.category, item.quantity, item.value,
                    item.condition, item.location, item.added_at
                ])

    def load_from_csv(self, filename):
        self.items.clear()
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = Item(
                    name=row["name"],
                    category=row["category"],
                    quantity=int(row["quantity"]),
                    value=float(row["value"]),
                    condition=row["condition"],
                    location=row["location"],
                )
                item.added_at = row["added_at"]
                self.items.append(item)



    def export_summary(self):
       
        summary = {}
        for item in self.items:
            summary[item.category] = summary.get(item.category, 0) + item.quantity
        return summary

    def filter_items(self, **kwargs):
    
        results = self.items
        for key, value in kwargs.items():
            results = [i for i in results if str(getattr(i, key)).lower() == str(value).lower()]
        return results

    def sort_items(self, key):
       
        return sorted(self.items, key=lambda x: getattr(x, key))
