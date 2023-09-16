import cv2
from mtcnn import MTCNN
import numpy as np
from keras.models import load_model
from random import choice

image_path = r"image4.jpg"
image = cv2.imread(image_path)

detector = MTCNN()
faces = detector.detect_faces(image)
emotion_model = load_model(r'model_v6_23.hdf5')
emotion_labels = {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}

colors = [(255,0,0), (0,255,0), (0,0,255), (255,0,255), (255,69,0), (0,128,0), (139,0,139)]

for face in faces:
    color = choice(colors)
    x, y, width, height = face['box']
    face_image = image[y: y+ height, x: x + width]
    face_image = cv2.resize(face_image, (48, 48))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = np.expand_dims(face_image, axis=0)
    face_image = np.expand_dims(face_image, axis=-1)
    predicted_class = np.argmax(emotion_model.predict(face_image))
    label_map = dict((v, k) for k, v in emotion_labels.items())
    predicted_label = label_map[predicted_class]
    cv2.rectangle(image, (x,y), (x+width,y+height), color, 2)
    cv2.putText(image, predicted_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


cv2.imwrite("final_image.jpg", image)
cv2.imshow('Detected faces and emotions', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


