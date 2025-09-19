
meds = [
    {"name": "Амоксицилін", "qty": 20, "category": "antibiotic", "temp": 22.0},
    {"name": "Вітамін C", "qty": 50, "category": "vitamin", "temp": 4.5},
    {"name": "Ковід-19 вакцина", "qty": 100, "category": "vaccine", "temp": 26.0},
    {"name": "Невідомий препарат", "qty": "десять", "category": "other", "temp": 18.0},
]

for med in meds:
    name = med.get("name")
    category = med.get("category")
    try:
        qty = int(med.get("qty"))     
        temp = float(med.get("temp")) 
    except (ValueError, TypeError):
        print(f"{name}: Помилка даних")
        continue

    
    if temp < 5:
        temp_status = "Надто холодно"
    elif temp > 25:
        temp_status = "Надто жарко"
    else:
        temp_status = "Норма"


    match category:
        case "antibiotic":
            cat_status = "Рецептурний препарат"
        case "vitamin":
            cat_status = "Вільний продаж"
        case "vaccine":
            cat_status = "Потребує спецзберігання"
        case _:
            cat_status = "Невідома категорія"

    print(f"{name}: {cat_status}, {temp_status}")

# %%
