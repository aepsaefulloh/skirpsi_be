import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from app.database import get_db_connection

level_mapping = {
    "Not Interested": 0,
    "Poor": 1,
    "Beginner": 2,
    "Average": 3,
    "Intermediate": 4,
    "Excellent": 5,
    "Professional": 6
}

def fetch_kejuruan_data():
    """ Mengambil data jawaban siswa dan kejuruan dari database """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT fa.user_id, fa.question_id, fa.answer_text, ka.kejuruan 
        FROM form_answers fa
        JOIN kejuruan_answers ka ON fa.user_id = ka.user_id
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return data

def preprocess_kejuruan_data():
    """ Mengubah data jawaban siswa menjadi format yang sesuai untuk KNN """
    data = fetch_kejuruan_data()

    X = []
    y = []
    user_answers = {}

    for row in data:
        user_id = row["user_id"]
        question_id = row["question_id"]
        answer_text = row["answer_text"]
        kejuruan = row["kejuruan"]

        if user_id not in user_answers:
            user_answers[user_id] = {"answers": {}, "kejuruan": kejuruan}

        user_answers[user_id]["answers"][question_id] = level_mapping.get(answer_text, 0)

    for user_id, details in user_answers.items():
        question_ids = sorted(details["answers"].keys())
        answer_vector = [details["answers"][qid] for qid in question_ids]
        X.append(answer_vector)
        y.append(details["kejuruan"])

    return np.array(X), np.array(y)


def train_kejuruan_knn():
    """ Melatih model KNN dengan data kejuruan """
    X, y = preprocess_kejuruan_data()

    if len(X) < 1:
        return None

    n_neighbors = min(3, len(X))  
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X, y)

    return knn

def predict_kejuruan(user_answers):
    """ Memprediksi kejuruan yang paling sesuai berdasarkan jawaban """
    knn = train_kejuruan_knn()

    if knn is None:
        return None 

    question_ids = sorted(user_answers.keys())
    input_vector = [level_mapping.get(user_answers[qid], 0) for qid in question_ids]

    prediction = knn.predict([input_vector])

    return prediction[0] 
