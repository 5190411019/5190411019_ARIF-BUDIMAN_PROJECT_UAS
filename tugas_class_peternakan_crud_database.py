import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="",  
            database="5190411019"
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabel untuk Hewan
        self.cursor.execute("CREATE TABLE IF NOT EXISTS hewan (id INT AUTO_INCREMENT PRIMARY KEY, nama VARCHAR(255), umur INT, jenis VARCHAR(255), pendapatan FLOAT)")

        # Tabel untuk Mamalia
        self.cursor.execute("CREATE TABLE IF NOT EXISTS mamalia (id INT AUTO_INCREMENT PRIMARY KEY, jenis_bulu VARCHAR(255), hewan_id INT, FOREIGN KEY (hewan_id) REFERENCES hewan(id))")

        # Tabel untuk Unggas
        self.cursor.execute("CREATE TABLE IF NOT EXISTS unggas (id INT AUTO_INCREMENT PRIMARY KEY, jenis_telur VARCHAR(255), hewan_id INT, FOREIGN KEY (hewan_id) REFERENCES hewan(id))")

        self.connection.commit()

    def tambah_data(self, hewan):
        if isinstance(hewan, Hewan):
            self.cursor.execute("INSERT INTO hewan (nama, umur, jenis, pendapatan) VALUES (%s, %s, %s, %s)", (hewan.get_nama(), hewan.umur, type(hewan).__name__, hewan.pendapatan))
            self.connection.commit()

            hewan_id = self.cursor.lastrowid

            if isinstance(hewan, Mamalia):
                self.cursor.execute("INSERT INTO mamalia (jenis_bulu, hewan_id) VALUES (%s, %s)", (hewan.jenis_bulu, hewan_id))
            elif isinstance(hewan, Unggas):
                self.cursor.execute("INSERT INTO unggas (jenis_telur, hewan_id) VALUES (%s, %s)", (hewan.get_jenis_telur(), hewan_id))

            self.connection.commit()
            print("Data hewan berhasil ditambahkan.")
        else:
            print("Objek yang ditambahkan bukan instance dari kelas Hewan.")

    def tampilkan_data(self):
        self.cursor.execute("SELECT hewan.id, hewan.nama, hewan.umur, hewan.jenis, hewan.pendapatan, mamalia.jenis_bulu, unggas.jenis_telur FROM hewan LEFT JOIN mamalia ON hewan.id = mamalia.hewan_id LEFT JOIN unggas ON hewan.id = unggas.hewan_id")
        data = self.cursor.fetchall()

        if not data:
            print("Tidak ada data hewan.")
        else:
            for row in data:
                print(f"ID: {row[0]}, Nama: {row[1]}, Umur: {row[2]}, Jenis: {row[3]}, Pendapatan: {row[4]}")

                if row[3] == 'Mamalia':
                    hewan = Mamalia(row[1], row[2], row[5], row[4])
                elif row[3] == 'Unggas':
                    hewan = Unggas(row[1], row[2], row[6], row[4])
                else:
                    print("Jenis hewan tidak valid.")
                    continue

                # Memanggil aktivitas_harian dari objek Hewan
                pendapatan = hewan.aktivitas_harian()

                # Menampilkan pendapatan
                print(f"Pendapatan Harian: {pendapatan}")

    def update_data(self, id, pendapatan_baru):
        self.cursor.execute("UPDATE hewan SET pendapatan = %s WHERE id = %s", (pendapatan_baru, id))
        self.connection.commit()
        print("Pendapatan hewan berhasil diupdate.")

    def hapus_data(self, id):
        self.cursor.execute("DELETE FROM hewan WHERE id = %s", (id,))
        self.connection.commit()
        print("Data hewan berhasil dihapus.")

    def __del__(self):
        try:
            self.cursor.close()
        except AttributeError:
            pass  # Ignore the error if cursor is not defined
        finally:
            try:
                self.connection.close()
            except AttributeError:
                pass 

# Tambahkan metode aktivitas_harian ke kelas Hewan
class Hewan:
    def __init__(self, nama, umur, pendapatan):
        self.__nama = nama
        self.umur = umur
        self.pendapatan = pendapatan

    def get_nama(self):
        return self.__nama

    def bersuara(self):
        print("Hewan bersuara: Suara hewan khas")

    def makan(self):
        print("Hewan sedang makan")

    def bergerak(self):
        print("Hewan sedang bergerak")

    def get_pendapatan(self):
        return self.pendapatan

    def aktivitas_harian(self):
        print(f"{self.get_nama()} adalah ternak.")
        self.makan()
        self.bergerak()
        self.bersuara()
        return self.get_pendapatan()

class Mamalia(Hewan):
    def __init__(self, nama, umur, jenis_bulu, pendapatan):
        super().__init__(nama, umur, pendapatan)
        self.jenis_bulu = jenis_bulu

    def menyusui(self):
        print(f"{self.get_nama()} menyusui anaknya")

    def bersuara(self):
        print("Mamalia bersuara: Suara mamalia khas")


# Kelas Anak Kedua: Unggas
class Unggas(Hewan):
    def __init__(self, nama, umur, jenis_telur, pendapatan):
        super().__init__(nama, umur, pendapatan)
        self.__jenis_telur = jenis_telur

    def bertelur(self):
        print(f"{self.get_nama()} sedang bertelur")

    def get_jenis_telur(self):
        return self.__jenis_telur

    def bersuara(self):
        print("Unggas bersuara: Kukuruyukk")


# Kelas Anak Kedua dari Mamalia: Sapi
class Sapi(Mamalia):
    def __init__(self, nama, umur, jenis_susu, pendapatan):
        super().__init__(nama, umur, "Berbulu lebat", pendapatan)
        self.jenis_susu = jenis_susu

    def bersuara(self):
        print("Sapi bersuara: Moo")

# Fungsi untuk mensimulasikan aktivitas harian di peternakan
def aktivitas_harian(hewan):
    print(f"{hewan.get_nama()} adalah ternak.")
    hewan.makan()
    hewan.bergerak()
    hewan.bersuara()
    hewan.get_pendapatan()

# Contoh penggunaan kelas dan konsep pewarisan, enkapsulasi, dan polimorfisme
db = Database()

# Contoh penggunaan CRUD
while True:
    print("\n===== Menu =====")
    print("1. Tambah Data Hewan (Mamalia/Unggas)")
    print("2. Tampilkan Data Hewan")
    print("3. Update Pendapatan Hewan")
    print("4. Hapus Data Hewan")
    print("5. Keluar")

    choice = int(input("Pilih menu (1-5): "))

    if choice == 1:
        print("\n===== Jenis Hewan =====")
        print("1. Mamalia")
        print("2. Unggas")
        jenis = input("Masukkan jenis hewan [1-2]: ").lower()

        if jenis == '1':
            nama = input("Masukkan nama mamalia: ")
            umur = int(input("Masukkan umur mamalia: "))
            jenis_bulu = input("Masukkan jenis bulu mamalia: ")
            pendapatan = float(input("Masukkan pendapatan mamalia: "))
            hewan = Mamalia(nama, umur, jenis_bulu, pendapatan)
            db.tambah_data(hewan)
        elif jenis == '2':
            nama = input("Masukkan nama unggas: ")
            umur = int(input("Masukkan umur unggas: "))
            jenis_telur = input("Masukkan jenis telur unggas: ")
            pendapatan = float(input("Masukkan pendapatan unggas: "))
            hewan = Unggas(nama, umur, jenis_telur, pendapatan)
            db.tambah_data(hewan)
        else:
            print("Jenis hewan tidak valid.")
    elif choice == 2:
        db.tampilkan_data()
    elif choice == 3:
        db.tampilkan_data()
        id_hewan = int(input("Masukkan ID hewan yang ingin diupdate: "))
        pendapatan_baru = float(input("Masukkan pendapatan baru: "))
        db.update_data(id_hewan, pendapatan_baru)
    elif choice == 4:
        db.tampilkan_data()
        id_hewan_hapus = int(input("Masukkan ID hewan yang ingin dihapus: "))
        db.hapus_data(id_hewan_hapus)
    elif choice == 5:
        print("Keluar dari program.")
        break
    else:
        print("Pilihan tidak valid. Silakan pilih lagi.")
