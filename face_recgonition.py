# face_recognition.py
import os
import face_recognition
import pickle

def encode_faces(images_path='student_images'):
    known_encodings = []
    known_roll_numbers = []

    for roll_number in os.listdir(images_path):
        student_folder = os.path.join(images_path, roll_number)
        for image_name in os.listdir(student_folder):
            image_path = os.path.join(student_folder, image_name)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                known_encodings.append(face_encodings[0])
                known_roll_numbers.append(roll_number)

    data = {"encodings": known_encodings, "roll_numbers": known_roll_numbers}
    
    with open("models/trained_model.pkl", "wb") as f:
        pickle.dump(data, f)

    print("Face encoding complete.")
