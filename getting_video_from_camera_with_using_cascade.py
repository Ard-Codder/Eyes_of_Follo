import cv2

capture = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('face_cascade/face_cascade.xml')

while True:
    ret, image = capture.read()

    faces = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=2, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255),
                      2)  # рисуем прямоугольник на месте найденного лица
    cv2.imshow('Web Camera', image)

    key = cv2.waitKey(30)
    if key == 27:  # 27 - это код клавиши Esc
        break

capture.release()
cv2.destroyAllWindows()
