import cv2

capture = cv2.VideoCapture(0)

while True:
    ret, image = capture.read()

    cv2.imshow('Web Camera', image)

    key = cv2.waitKey(30)
    if key == 27:  # 27 - это код клавиши Esc
        break

capture.release()
cv2.destroyAllWindows()
