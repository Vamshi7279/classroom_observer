import face_recognition
import os
import pickle
import cv2

image_dir = "student_images"
known_encodings = []
roll_numbers = []

for folder in os.listdir(image_dir):
    folder_path = os.path.join(image_dir, folder)
    if not os.path.isdir(folder_path) or folder.startswith('.'):
        continue
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        if not (img_name.endswith(".jpg") or img_name.endswith(".jpeg") or img_name.endswith(".png")):
            continue  # Skip non-image files

        image = cv2.imread(img_path)
        if image is None:
            print(f"⚠️ Skipping unreadable image: {img_path}")
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            roll_numbers.append(folder)

data = {"encodings": known_encodings, "roll_numbers": roll_numbers}

os.makedirs("models", exist_ok=True)
with open("models/trained_model.pkl", "wb") as f:
    pickle.dump(data, f)

print("✅ Model trained and saved to models/trained_model.pkl")
