class JunkItem:
    def __init__(self, name, quantity, value):
        self.name = name
        self.quantity = quantity
        self.value = value
    
    def __str__(self):
        return f"{self.name} (кількість: {self.quantity}, вартість: {self.value})"


class JunkStorage:
    def __init__(self):
        self.items = []
    def serialize(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:  
                file.write("name,quantity,value\n")
                for item in self.items:
                    file.write(f"{item.name},{item.quantity},{item.value}\n")
            print(f"Дані збережено у {filename}")
        except Exception as e:
            print(f"Помилка: {e}")

    def parse(self, filename):
        self.items = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()                 
                for line in lines[1:]:
                    line = line.strip()  
                    if not line:  
                        continue                               
                    parts = line.split(',')                 
                    if len(parts) != 3:
                        print(f"Пропущено некоректний рядок: {line}")
                        continue
                    
                    try:
                        name = parts[0].strip()
                        quantity = int(parts[1].strip())
                        value = float(parts[2].strip())                      
                        if not name:
                            print(f"Пропущено рядок без назви")
                            continue                
                        item = JunkItem(name, quantity, value)
                        self.items.append(item)
                    except ValueError:
                        print(f"Помилка формату у рядку: {line}")
                        continue
            
            print(f"Завантажено {len(self.items)} предметів")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено")
        except Exception as e:
            print(f"Помилка: {e}")

def main():
    storage = JunkStorage()
    print("Створення предметів")
    storage.items.append(JunkItem("Бляшанка", 5, 2.5))
    storage.items.append(JunkItem("Стара плата", 3, 7.8))
    storage.items.append(JunkItem("Купка дротів", 10, 1.2))
    
    for item in storage.items:
        print(f"Створено: {item}")
    print("\nЗбереження")
    storage.serialize('junk_items.csv')
    storage.items = []
    print(f"\nСписок очищено. Предметів: {len(storage.items)}")
    print("\nЗавантаження ")
    storage.parse('junk_items.csv') 
    print("\nРезультат ")
    for item in storage.items:
        print(item)
if __name__ == "__main__":
    main()