import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def analyze_data(csv_path):
    
    data = pd.read_csv(csv_path)

    
    avg_price = np.mean(data['price_per_unit'])
    median_quantity = np.median(data['quantity'])
    std_price = np.std(data['price_per_unit'])

    
    data['total_price'] = data['quantity'] * data['price_per_unit']

    profit_by_supplier = data.groupby('supplier')['total_price'].sum()
    best_supplier = profit_by_supplier.idxmax()
    best_profit = profit_by_supplier.max()

    quantity_by_category = data.groupby('category')['quantity'].sum()

  
    low_supply = data[data['quantity'] < 100]
    low_supply_file = "low_supply.csv"
    low_supply.to_csv(low_supply_file, index=False)


    report_text = f"""ЗВІТ ПРО ПОСТАЧАННЯ

Середня ціна: {avg_price:.2f}
Медіана кількості: {median_quantity}
Стандартне відхилення ціни: {std_price:.2f}

Постачальник з найбільшим прибутком: {best_supplier} ({best_profit:.2f})

Файл із малими залишками: {low_supply_file}
"""

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

   
    plt.figure(figsize=(8, 5))
    quantity_by_category.plot(kind='bar')
    plt.title("Кількість препаратів за категоріями")
    plt.xlabel("Категорія")
    plt.ylabel("Загальна кількість")
    plt.tight_layout()
    plt.savefig("category_distribution.png")
    plt.close()

    print("Аналіз виконано. Результати збережено у файли:")
    print(" - report.txt")
    print(" - low_supply.csv")
    print(" - category_distribution.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Аналіз даних постачань")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="supplies.csv",
       
    )
    args = parser.parse_args()

    if os.path.exists(args.csv_path):
        analyze_data(args.csv_path)
    else:
        print("Файл не знайдено:", args.csv_path)
