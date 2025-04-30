import time
import random
from collections import deque

class Document:
    def __init__(self, name, priority=False):
        self.name = name
        self.size = random.randint(1, 10)  # ukuran MB
        self.type = self.determine_type()
        self.priority = priority  # True untuk dokumen prioritas

    def determine_type(self):
        if self.name.endswith(".pdf"):
            return "PDF"
        elif self.name.endswith(".docx"):
            return "Word"
        elif self.name.endswith(".xlsx"):
            return "Excel"
        else:
            return "Lainnya"

    def __str__(self):
        prioritas = " (Prioritas)" if self.priority else ""
        return f"{self.name} ({self.type}, {self.size}MB){prioritas}"

class PrinterQueue:
    def __init__(self):
        self.queue = deque()
        self.history = []

    def enqueue(self, document):
        if document.priority:
            self.queue.appendleft(document)
            print(f"Dokumen prioritas '{document.name}' masuk ke depan antrian.\n")
        else:
            self.queue.append(document)
            print(f"Dokumen '{document.name}' masuk ke antrian.\n")

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        else:
            print("Antrian kosong.\n")
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def show_queue(self):
        if self.is_empty():
            print("\nAntrian kosong.\n")
        else:
            print("\n=== Daftar Antrian Dokumen ===")
            for idx, doc in enumerate(self.queue, 1):
                print(f"{idx}. {doc}")
            print("===============================\n")

    def clear(self):
        self.queue.clear()
        print("Antrian telah dikosongkan.\n")

    def add_history(self, document, status):
        self.history.append((document, status))

    def show_history(self):
        if not self.history:
            print("\nBelum ada histori cetakan.\n")
        else:
            print("\n=== Histori Cetakan ===")
            for idx, (doc, status) in enumerate(self.history, 1):
                print(f"{idx}. {doc.name} - {status}")
            print("=========================\n")

class PrinterApp:
    def __init__(self):
        self.printer_queue = PrinterQueue()

    def menu(self):
        while True:
            self.show_menu()
            pilihan = input("Pilih menu (1-7): ").strip()

            if pilihan == '1':
                self.add_documents()
            elif pilihan == '2':
                self.printer_queue.show_queue()
            elif pilihan == '3':
                self.print_one()
            elif pilihan == '4':
                self.print_all()
            elif pilihan == '5':
                self.printer_queue.show_history()
            elif pilihan == '6':
                self.printer_queue.clear()
            elif pilihan == '7':
                print("Terima kasih telah menggunakan aplikasi printer!\n")
                break
            else:
                print("Pilihan tidak valid. Coba lagi.\n")

    def show_menu(self):
        print("=" * 50)
        print("         APLIKASI SIMULATOR PRINTER v2.0")
        print("=" * 50)
        print("1. Tambah Dokumen ke Antrian")
        print("2. Tampilkan Antrian")
        print("3. Cetak Satu Dokumen")
        print("4. Cetak Semua Dokumen")
        print("5. Lihat Histori Cetakan")
        print("6. Kosongkan Antrian")
        print("7. Keluar")
        print("=" * 50)

    def add_documents(self):
        try:
            jumlah = int(input("Berapa dokumen yang ingin ditambahkan? "))
            for _ in range(jumlah):
                nama = input("Masukkan nama dokumen (misal: tugas.pdf): ").strip()
                prioritas_input = input("Apakah dokumen ini prioritas? (y/n): ").strip().lower()
                prioritas = prioritas_input == 'y'
                doc = Document(nama, priority=prioritas)
                self.printer_queue.enqueue(doc)
        except ValueError:
            print("Input tidak valid. Masukkan angka.\n")

    def print_one(self):
        doc = self.printer_queue.dequeue()
        if doc:
            self.simulate_print(doc)

    def print_all(self):
        if self.printer_queue.is_empty():
            print("Tidak ada dokumen untuk dicetak.\n")
            return
        while not self.printer_queue.is_empty():
            doc = self.printer_queue.dequeue()
            self.simulate_print(doc)

    def simulate_print(self, document):
        print(f"\nSedang mencetak: {document}")
        estimated_time = document.size * 0.4  # 0.4 detik per MB
        print(f"Estimasi waktu cetak: {estimated_time:.1f} detik")
        
        # Simulasi kemungkinan error
        error_occurred = random.choice([False, False, False, True])  # 25% error chance
        if error_occurred:
            error_type = random.choice(["Tinta habis", "Kertas macet"])
            print(f"!!! ERROR: {error_type} saat mencetak '{document.name}'\n")
            self.printer_queue.add_history(document, f"Gagal - {error_type}")
            return

        for i in range(1, document.size + 1):
            print(f"Progress: {(i / document.size) * 100:.0f}%")
            time.sleep(0.4)

        print(f"Dokumen '{document.name}' berhasil dicetak!\n")
        self.printer_queue.add_history(document, "Berhasil")

if __name__ == "__main__":
    app = PrinterApp()
    app.menu()