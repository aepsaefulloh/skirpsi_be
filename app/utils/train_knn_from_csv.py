import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import accuracy_score
import joblib

# Path ke file CSV dan Model KNN
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../database/dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "knn_model.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")

def train_knn_from_csv():
    """ Melatih model KNN dari dataset CSV dengan normalisasi dan menyimpan model """
    
    # 1️⃣ Baca file CSV
    if not os.path.exists(CSV_FILE_PATH) or os.stat(CSV_FILE_PATH).st_size == 0:
        print("❌ Dataset CSV tidak ditemukan atau kosong. Harap tambahkan data!")
        return None, None, None, 0.0

    df = pd.read_csv(CSV_FILE_PATH)

    # 2️⃣ Pastikan dataset memiliki cukup data untuk training
    if len(df) < 10:
        print("❌ Data terlalu sedikit untuk training model KNN. Harap tambahkan lebih banyak data!")
        return None, None, None, 0.0

    # 3️⃣ Pastikan semua jawaban adalah angka (answer_index)
    for col in df.columns[:-1]:  # Semua kolom kecuali "Kejuruan"
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4️⃣ Pisahkan fitur (X) dan target (y)
    X = df.iloc[:, :-1]  # Semua kolom kecuali kolom terakhir (Kejuruan)
    y = df.iloc[:, -1]   # Kolom terakhir (Kejuruan)

    # 5️⃣ Encode label target agar berbentuk numerik
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # 6️⃣ Bagi data menjadi training (80%) & testing (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # 7️⃣ Normalisasi fitur menggunakan MinMaxScaler
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 8️⃣ Latih model KNN
    k = min(2, len(X_train))  # Gunakan max(k=3) atau jumlah sampel minimum
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)

    # 9️⃣ Prediksi pada data testing
    y_pred = knn.predict(X_test)

    # 🔟 Hitung akurasi model
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"✅ Akurasi Model KNN setelah normalisasi: {accuracy:.2f}%")

    # 🔟 Simpan model, encoder, dan scaler agar tidak perlu training ulang setiap prediksi
    joblib.dump(knn, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print("✅ Model KNN, Label Encoder, dan Scaler berhasil disimpan!")

    return knn, label_encoder, scaler, accuracy  # Return model dan akurasi

def load_trained_model():
    """ Memuat model KNN, Label Encoder, dan Scaler jika sudah tersedia """
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH) and os.path.exists(SCALER_PATH):
        knn = joblib.load(MODEL_PATH)
        label_encoder = joblib.load(ENCODER_PATH)
        scaler = joblib.load(SCALER_PATH)
        print("✅ Model KNN berhasil dimuat!")
        return knn, label_encoder, scaler
    else:
        print("⚠️ Model belum ada, melakukan training ulang...")
        return train_knn_from_csv()

def predict_kejuruan_from_csv(user_answers):
    """ Memprediksi kejuruan berdasarkan jawaban user baru """
    knn, label_encoder, scaler = load_trained_model()

    if knn is None or label_encoder is None or scaler is None:
        return "❌ Model belum siap, harap latih ulang dengan dataset yang cukup!"

    # Gunakan jawaban numerik langsung (answer_index) tanpa LEVEL_MAPPING
    input_vector = np.array(user_answers).reshape(1, -1)

    # **Gunakan scaler yang telah dilatih untuk menormalisasi input user**
    input_vector = scaler.transform(input_vector)

    # Prediksi kejuruan
    prediction = knn.predict(input_vector)

    # Ubah hasil prediksi ke label aslinya
    predicted_kejuruan = label_encoder.inverse_transform(prediction)[0]

    return predicted_kejuruan
