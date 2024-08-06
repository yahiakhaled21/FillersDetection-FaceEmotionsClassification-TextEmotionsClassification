import cv2
import numpy as np
from keras.models import model_from_json
def main(video_path):
    with open('InstaJobApp\Scripts\Face\Models\model77.json', 'r') as json_file:
        model_json = json_file.read()
    emotion_model = model_from_json(model_json)

    emotion_model.load_weights('InstaJobApp\Scripts\Face\Models\model77.weights.h5')
    print("Loaded model from disk")

    emotion_dict = {0: "Angry", 1: "Happy", 2: "Neutral", 3: "Sad"}


    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    emotion_counts = {emotion: 0 for emotion in emotion_dict.values()}
    total_frames = 0
    score = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cropped_face = gray[y:y+h, x:x+w]

            resized_face = cv2.resize(cropped_face, (48, 48))

            input_image = np.expand_dims(resized_face, axis=0)
            input_image = np.expand_dims(input_image, axis=3)  

            input_image = input_image / 255.0

            emotion_prediction = emotion_model.predict(input_image)

            predicted_emotion = emotion_dict[np.argmax(emotion_prediction)]
            print("Predicted Emotion:", predicted_emotion)

            emotion_counts[predicted_emotion] += 1
            total_frames += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.putText(frame, predicted_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            if predicted_emotion in ["Angry", "Sad"]:
                score += 1

        cv2.imshow('Emotion Detection', frame)

        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Emotion Counts:")
    for emotion, count in emotion_counts.items():
        percentage = (count / total_frames) * 100 if total_frames != 0 else 0
        print(f"{emotion}: {count} ({percentage:.2f}%)")

    print("Calculating Score...")
    print("Score:", score)
    return score