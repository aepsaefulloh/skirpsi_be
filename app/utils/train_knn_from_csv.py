import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import os

# Path ke file CSV
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../database/dataset.csv")

def train_knn_from_csv():
    """ Melatih model KNN menggunakan data dari file CSV """

    # 1️⃣ Baca file CSV
    df = pd.read_csv(CSV_FILE_PATH)

    # 2️⃣ Pisahkan fitur (X) dan target (y)
    X = df.iloc[:, :-1]  # Semua kolom kecuali kolom terakhir (Kejuruan)
    y = df.iloc[:, -1]   # Kolom terakhir (Kejuruan)

    # 3️⃣ Encode label target agar berbentuk numerik
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # 4️⃣ Bagi data menjadi training (80%) dan testing (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # 5️⃣ Latih model KNN
    k = 3  # Jumlah tetangga terdekat
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)

    # 6️⃣ Evaluasi akurasi model
    accuracy = knn.score(X_test, y_test) * 100
    print(f"✅ Akurasi Model KNN: {accuracy:.2f}%")

    return knn, label_encoder  # Return model dan encoder label

def predict_kejuruan_from_csv(user_answers):
    """ Memprediksi kejuruan berdasarkan jawaban user baru """
    knn, label_encoder = train_knn_from_csv()

    # Pastikan input user memiliki jumlah fitur yang sama dengan data training
    input_vector = np.array(user_answers).reshape(1, -1)

    # Prediksi kejuruan
    prediction = knn.predict(input_vector)

    # Ubah hasil prediksi ke label aslinya
    predicted_kejuruan = label_encoder.inverse_transform(prediction)[0]

    return predicted_kejuruan

if __name__ == "__main__":
    # Contoh input dari user baru (harus dalam bentuk list dengan panjang sama dengan fitur di CSV)
    user_baru = [6, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Contoh data input user baru
    hasil_prediksi = predict_kejuruan_from_csv(user_baru)
    print(f"🔮 Prediksi Kejuruan untuk User Baru: {hasil_prediksi}")
