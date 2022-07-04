from cv2 import cv2
import argparse

# Чтобы из терминала можно было передавать путь к изображению, добавим argparse
'''ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())'''

img = 'Image.jpg'
# Прочитаем изображение
image = cv2.imread(img, cv2.AgastFeatureDetector_OAST_9_16)
cv2.imshow("Image", image)
cv2.waitKey(0)

# Вывод размеров изображения
(h, w) = image.shape[:2]
print("width: {} pixels".format(w))
print("height: {} pixels".format(h))

# Запись изображения по указанному пути
cv2.imwrite("folder/newimage.png", image)
