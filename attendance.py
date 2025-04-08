# attendance.py
import face_recognition
import cv2
import pickle
import datetime
import pandas as pd
import os
import numpy as np

def take_attendance():
    with open("models/trained_model.pkl", "rb") as f:
        data = pickle.load(f)

    video = cv2.VideoCapture(0)
    recognized_today = set()
    today = datetime.date.today().strftime("%Y-%m-%d")

    attendance_file = "data/attendance.csv"
    if not os.path.exists(attendance_file):
        df = pd.DataFrame(columns=["Date", "Roll Number", "Status"])
        df.to_csv(attendance_file, index=False)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Resize frame to 1/4 size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Use 'cnn' model for better accuracy
        face_locations = face_recognition.face_locations(rgb_frame, model='cnn')
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding in face_encodings:
            distances = face_recognition.face_distance(data["encodings"], encoding)
            best_match_index = np.argmin(distances)
            if distances[best_match_index] < 0.45:  # Stricter tolerance
                roll_number = data["roll_numbers"][best_match_index]
                if roll_number not in recognized_today:
                    recognized_today.add(roll_number)
                    df = pd.read_csv(attendance_file)
                    new_row = pd.DataFrame([{
                        "Date": today,
                        "Roll Number": roll_number,
                        "Status": "Present"
                    }])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv(attendance_file, index=False)
                    print(f"Marked present: {roll_number}")

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
