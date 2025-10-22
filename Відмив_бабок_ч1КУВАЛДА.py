def shadow(limit=200):
    def decorator(generator_func):
        def wrapper(*args, **kwargs):
            total_sum = 0
            limit_breached = False
            
            source_stream = generator_func(*args, **kwargs)
            
            for item in source_stream:
                try:
                    parts = item.split()
                    action, amount_str = parts[0], parts[1]
                    amount = int(amount_str)
                    
                    if action in ("payment", "transfer", "refund"):
                        total_sum += amount
                    else:
                        continue
                
                except (ValueError, IndexError):
                    continue
                
                if not limit_breached and total_sum > limit:
                    print(f"\n[СХЕМА]: Тіньовий ліміт ({limit}) пробито. Активація протоколів.\n")
                    limit_breached = True
                
                yield item
            
            return total_sum
            
        return wrapper
    return decorator


@shadow(limit=400)
def transaction_stream():
    transactions = [
        "payment 120",
        "refund 50",
        "noise data ignore this",
        "transfer 300",
        "payment 25",
        "system_log non-numeric",
        "unknown_op 100"
    ]
    for t in transactions:
        print(f"[ПОТІК]: Згенеровано транзакцію -> '{t}'")
        yield t


if __name__ == "__main__":
    print("--- Активація тіньового моніторингу ---\n")
    
    monitored_stream = transaction_stream()
    final_balance = 0

    try:
        while True:
            transaction_data = next(monitored_stream)
            print(f"   [ЗОВНІШНІЙ СВІТ]: Отримано дані: '{transaction_data}'")
            
    except StopIteration as e:
        final_balance = e.value
        print("\n--- Потік вичерпано. Моніторинг завершено. ---")

    print(f"\nФінальний тіньовий баланс: {final_balance}")