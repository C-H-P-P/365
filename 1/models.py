from abc import ABC, abstractmethod


class Medicine(ABC):
    def __init__(self, name, quantity, price):
      
        if type(name) is not str:
            raise TypeError("Поле name повинно бути типу str")
        if type(quantity) is not int:
            raise TypeError("Поле quantity повинно бути цілим числом")
        if quantity <= 0:
            raise ValueError("Quantity має бути більше 0")
        if type(price) not in [int, float]:
            raise TypeError("Поле price повинно бути числом (int або float)")
        if price <= 0:
            raise ValueError("Price має бути більше 0")

        
        self.name = name
        self.quantity = quantity
        self.price = price

    
    @abstractmethod
    def requires_prescription(self):
        pass

    @abstractmethod
    def storage_requirements(self):
        pass

    def total_price(self):
        total = self.quantity * self.price
        return total

    @abstractmethod
    def info(self):
        pass



class Antibiotic(Medicine):
    def requires_prescription(self):
        return True

    def storage_requirements(self):
        return "8–15°C, темне місце"

    def info(self):
        text = "Антибіотик: " + str(self.name)
        text += ", кількість: " + str(self.quantity)
        text += ", ціна: " + str(self.price) + " грн"
        text += ", потрібен рецепт: " + str(self.requires_prescription())
        text += ", умови зберігання: " + self.storage_requirements()
        text += ", загальна вартість: " + str(self.total_price()) + " грн"
        return text


class Vitamin(Medicine):
    def requires_prescription(self):
        return False

    def storage_requirements(self):
        return "15–25°C, сухо"

    def info(self):
        return f"Вітамін: {self.name}, кількість: {self.quantity}, ціна: {self.price} грн, рецепт: {self.requires_prescription()}, умови зберігання: {self.storage_requirements()}, загальна вартість: {self.total_price()} грн"



class Vaccine(Medicine):
    def requires_prescription(self):
        return True

    def storage_requirements(self):
        return "2–8°C, холодильник"

    def total_price(self):
      
        base_total = super().total_price()
        new_total = base_total + base_total * 0.1
        return new_total

    def info(self):
        return ("Вакцина: " + self.name + ", кількість: " + str(self.quantity) +
                ", ціна: " + str(self.price) + " грн" +
                ", рецепт: " + str(self.requires_prescription()) +
                ", умови зберігання: " + self.storage_requirements() +
                ", загальна вартість (з 10%): " + str(round(self.total_price(), 2)) + " грн")
