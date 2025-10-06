import abc

class Document(abc.ABC):
    @abc.abstractmethod
    def render(self) -> str:
        pass

class Report(Document):
    def render(self) -> str:
        return "Це звіт. Якийсь формат."

class Invoice(Document):
    def render(self) -> str:
        return "Це рахунок. Табличка з цифрами."

class Contract(Document):
    def render(self) -> str:
        return "Це контракт. Нудний текст."

class NullDocument(Document):
    def render(self) -> str:
        return "Невідомий документ, сорі."

class DocumentFactory:
    @staticmethod
    def create(doc_type: str) -> Document:
        if doc_type == 'report':
            return Report()
        elif doc_type == 'invoice':
            return Invoice()
        elif doc_type == 'contract':
            return Contract()
        else:
            return NullDocument()

def client_code(doc_type: str):
    document = DocumentFactory.create(doc_type)
    print(f"Створюємо: {doc_type}")
    print(document.render())
    print("-" * 20)

if __name__ == "__main__":
    client_code('report')
    client_code('invoice')
    client_code('contract')
    client_code('diploma')
    client_code('test')