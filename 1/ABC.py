from models import Antibiotic, Vitamin, Vaccine

def main():
    medicines = []
    medicines.append(Antibiotic("Амоксицилін", 10, 10))
    medicines.append(Vitamin("Вітамін C", 10, 10))
    medicines.append(Vaccine("Кір", 510, 10))

    for med in medicines:
        print("===")
        print(med.info())
if __name__ == "__main__":
    main()
