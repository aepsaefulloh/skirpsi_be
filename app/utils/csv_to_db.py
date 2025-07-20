# app/utils/csv_to_db.py
import pandas as pd
import os
import random
from app.database import get_db_connection

# Path file CSV
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../database/dataset.csv")

# Daftar jawaban yang diperbolehkan
ANSWER_CHOICES = [
    "Not Interested", "Poor", "Beginner", "Average",
    "Intermediate", "Excellent", "Professional"
]

KEJURUAN_LIST = [
    "Software Engineer", "Network Engineer", "Database Administrator"
]

# Header sesuai struktur data
COLUMNS = [
    "Programming Skill", "Database Fundamentals", "Computer Architecture",
    "Cyber Security", "Computer Networking", "Project Management", "Kejuruan"
]

def generate_dummy_data(num_users=150):
    """Generate dummy user data dengan menyimpan answer_index (1-7), bukan 0-6."""
    return [
        [random.randint(1, len(ANSWER_CHOICES)) for _ in range(6)] + [random.choice(KEJURUAN_LIST)]
        for _ in range(num_users)
    ]

def save_dummy_data_to_csv():
    """Simpan data dummy ke file CSV jika file kosong."""
    if not os.path.exists(CSV_FILE_PATH) or os.stat(CSV_FILE_PATH).st_size == 0:
        df = pd.DataFrame(generate_dummy_data(), columns=COLUMNS)
        df.to_csv(CSV_FILE_PATH, index=False)
        print("✅ File CSV berhasil dibuat dengan 150 data dummy (answer_index mulai dari 1)!") 
    else:
        print("⚠️ File CSV sudah ada, tidak di-overwrite.")

def insert_csv_to_db():
    """Membaca file CSV dan memasukkan data ke database dengan answer_index mulai dari 1."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        df = pd.read_csv(CSV_FILE_PATH)

        # Cek apakah 150 user sudah ada di tabel users
        cursor.execute("SELECT COUNT(*) FROM users")
        existing_users = cursor.fetchone()[0]

        if existing_users >= 150:
            print("⚠️ Dummy users sudah ada, tidak menambahkan data baru.")
            return

        # Ambil daftar question_id yang valid dari `form_questions`
        cursor.execute("SELECT id FROM form_questions")
        valid_question_ids = [row[0] for row in cursor.fetchall()]

        if not valid_question_ids:
            print("❌ Tidak ada pertanyaan di tabel `form_questions`.")
            return

        # Query untuk insert data
        user_insert_query = """
            INSERT INTO users (id, username, password, fullname, email, date_of_birth, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=id
        """

        kejuruan_insert_query = """
            INSERT INTO kejuruan_answers (user_id, kejuruan)
            VALUES (%s, %s) ON DUPLICATE KEY UPDATE kejuruan = VALUES(kejuruan)
        """

        form_answer_insert_query = """
            INSERT INTO form_answers (form_id, question_id, user_id, answer_index, answer_text, kejuruan)
            VALUES (%s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE answer_index = VALUES(answer_index), answer_text = VALUES(answer_text)
        """

        for index, row in df.iterrows():
            user_id = index + 1
            form_id = 1
            kejuruan = row["Kejuruan"]
            answers = row[:-1].values.tolist()  # Ambil hanya nilai answer_index dari CSV

            # Insert user jika belum ada
            cursor.execute(user_insert_query, (
                user_id, f"user{user_id}", "$2b$12$7z5ZoMQafiGmIezuhfg6PO.n9NMN9A2GtFhduwT8GGWFK.J2qkUO2", f"User {user_id}",
                f"user{user_id}@mail.com", "2000-01-01", 99
            ))

            # Insert kejuruan jika belum ada
            cursor.execute(kejuruan_insert_query, (user_id, kejuruan))

            # Insert jawaban ke form_answers
            for i, question_id in enumerate(valid_question_ids[:len(answers)]):
                answer_index = int(answers[i])  # Pastikan integer
                answer_text = ANSWER_CHOICES[answer_index - 1]  # Konversi index ke teks

                cursor.execute(form_answer_insert_query, (
                    form_id, question_id, user_id, answer_index, answer_text, kejuruan
                ))

        conn.commit()
        print("✅ Data dari CSV berhasil disimpan ke database dengan answer_index (1-7)!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Terjadi kesalahan: {e}")
    finally:
        cursor.close()
        conn.close()

# Eksekusi fungsi
save_dummy_data_to_csv()
insert_csv_to_db()
