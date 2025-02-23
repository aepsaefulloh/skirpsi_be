import pandas as pd
from app.database import get_db_connection
import os

# Path file CSV
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../database/dataset.csv")

# Data dummy untuk diisi ke dalam CSV
dummy_data = [
    [6, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "Database Administrator"],
    [5, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, "Software Engineer"],
    [4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, "Cyber Security"],
    [3, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "Network Engineer"],
    [2, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, "Data Scientist"]
]

# Header sesuai struktur data
columns = ["Database", "Computer", "Distribute", "Cyber Sec", "Networking", "Software",
           "Programming", "Project M", "Technical", "AI ML", "Software", "Business",
           "Communication", "Data Science", "Troubleshooting", "Graphics", "Kejuruan"]

# Simpan data ke CSV jika file kosong
if not os.path.exists(CSV_FILE_PATH) or os.stat(CSV_FILE_PATH).st_size == 0:
    df = pd.DataFrame(dummy_data, columns=columns)
    df.to_csv(CSV_FILE_PATH, index=False)
    print("✅ File CSV berhasil dibuat dengan data dummy!")
else:
    print("⚠️ File CSV sudah ada, tidak di-overwrite.")

def insert_csv_to_db():
    """ Membaca file CSV dan memasukkan data ke database """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Baca kembali file CSV yang sudah berisi data
    df = pd.read_csv(CSV_FILE_PATH)

    # ✅ Pastikan User ID ada di tabel `users` sebelum dimasukkan ke `kejuruan_answers`
    for index, row in df.iterrows():
        user_id = index + 1

        # Cek apakah user sudah ada di tabel `users`
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        # Jika user belum ada, tambahkan user dummy
        if not user:
            cursor.execute("INSERT INTO users (id, username, password, fullname, email, date_of_birth, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (user_id, f"user{user_id}", "password123", f"User {user_id}", f"user{user_id}@mail.com", "2000-01-01", 1))
            print(f"✅ User {user_id} berhasil ditambahkan!")

        # Masukkan data ke `kejuruan_answers`
        cursor.execute(
            "INSERT INTO kejuruan_answers (user_id, kejuruan) VALUES (%s, %s) ON DUPLICATE KEY UPDATE kejuruan = VALUES(kejuruan)",
            (user_id, row["Kejuruan"])
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data dari CSV berhasil disimpan ke database!")
