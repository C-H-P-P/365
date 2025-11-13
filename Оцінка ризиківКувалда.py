import threading
import random
import time
from tqdm import tqdm


PRICE_PER_UNIT = 50

class Warehouse:
    def __init__(self, name, initial_meds):
        self.name = name
        self.meds = initial_meds
        self.initial_meds = initial_meds
        self.lock = threading.Lock()

    def steal(self, amount, runner_name):
        with self.lock:
            if self.meds <= 0:
                return 0, "порожньо"

          
            outcome = random.choices(
                ["успіх", "частковий_успіх", "спіймали", "провал"],
                weights=[50, 25, 15, 10], k=1
            )[0]

            if outcome == "спіймали":
                return 0, "спіймали"
            elif outcome == "провал":
                return 0, "провал"
            elif outcome == "частковий_успіх":
                stolen = random.randint(1, min(amount // 2, self.meds))
            else:  
                stolen = min(amount, self.meds)

            self.meds -= stolen
            return stolen, "успіх" if stolen == amount else "частково"

    def __str__(self):
        return f"{self.name}: {self.meds}/{self.initial_meds} медикаментів"


class Runner(threading.Thread):
    def __init__(self, warehouse, name, progress_bar):
        super().__init__()
        self.warehouse = warehouse
        self.name = name
        self.progress_bar = progress_bar
        self.profit = 0
        self.stolen_total = 0

    def run(self):
        for _ in range(10):
            amount = random.randint(10, 30)
            stolen, status = self.warehouse.steal(amount, self.name)

            if stolen > 0:
                self.profit += stolen * PRICE_PER_UNIT
                self.stolen_total += stolen

            self.progress_bar.update(1)
            time.sleep(random.uniform(0.1, 0.5))

def run_simulation(num_runners, warehouses):
    print(f"\n{'='*60}")
    print(f"СИМУЛЯЦІЯ: {num_runners} БІГУНІВ")
    print(f"{'='*60}")

    
    total_attempts = num_runners * 10
    progress_bars = [
        tqdm(total=10, desc=f"{f'Бігун {i+1}':<10}", position=i, leave=False)
        for i in range(num_runners)
    ]

    runners = []
    for i in range(num_runners):
        warehouse = random.choice(warehouses)
        runner = Runner(warehouse, f"Бігун {i+1}", progress_bars[i])
        runners.append(runner)

    
    for r in runners:
        r.start()

    for r in runners:
        r.join()


    for pb in progress_bars:
        pb.close()


    total_profit = sum(r.profit for r in runners)
    print("\nЗВІТ:")
    print("-" * 50)
    for w in warehouses:
        loss = w.initial_meds - w.meds
        print(f"{w}")
        print(f"   Втрачено: {loss} од. ({loss/w.initial_meds*100:.1f}%)")
    print("-" * 50)
    print(f"Загальний прибуток: {total_profit:,} грн")
    print(f"Середній заробіток на бігуна: {total_profit // num_runners if num_runners > 0 else 0:,} грн")
    return total_profit



if __name__ == "__main__":
    random.seed(time.time())
    print("ЗАПУСК СИМУЛЯЦІЇ КРАДІЖКИ МЕДИКАМЕНТІВ")
   

    
    warehouse_names = ["Центральний", "Північний", "Промзона", "Лікарня №5", "Склад на околиці"]
    warehouses = [
        Warehouse(name, random.randint(100, 300)) for name in warehouse_names
    ]

    print("СКЛАДИ:")
    for w in warehouses:
        print(f"  {w.name}: {w.meds} медикаментів")
    print()

   
    results = []
    for num_runners in range(3, 8):
        for w in warehouses:
            w.meds = w.initial_meds
            w.lock = threading.Lock()
        profit = run_simulation(num_runners, warehouses)
        results.append((num_runners, profit))

 
    print("\n" + "="*60)
    print("ПІДСУМКОВИЙ АНАЛІЗ: СКІЛЬКИ БІГУНІВ НАЙМАТИ?")
    print("="*60)
    print(f"{'Бігуни':<8} {'Прибуток':<12} {'Прибуток/бігуна':<16} {'Ризик'}")
    print("-" * 50)

    for runners, profit in results:
        per_runner = profit // runners
        risk = "Низький" if runners <= 4 else "Середній" if runners <= 6 else "Високий"
        print(f"{runners:<8} {profit:>10,} грн {per_runner:>12,} грн {'':>8} {risk}")

    best = max(results, key=lambda x: x[1] / x[0])  
    print(f"\nОПТИМАЛЬНО: {best[0]} бігунів → {best[1]:,} грн (найвищий заробіток на одного)")
