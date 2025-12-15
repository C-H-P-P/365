import threading
import queue
import time

class EventProcessor:
    def __init__(self, workers=2):
        self.queue = queue.Queue()
        self.workers = []
        self.running = True

        for _ in range(workers):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            self.workers.append(t)

    def _worker(self):
        while self.running or not self.queue.empty():
            try:
                event = self.queue.get(timeout=0.5)
                self.handle_event(event)
                self.queue.task_done()
            except queue.Empty:
                pass

    def handle_event(self, event):
        print(f"Обробка події: {event}")
        time.sleep(1)

    def add_event(self, event):
        self.queue.put(event)

    def stop(self):
        self.running = False
        self.queue.join()


processor = EventProcessor(workers=3)

for i in range(10):
    processor.add_event(f"Event {i}")

processor.stop()
print("Всі події оброблено")
