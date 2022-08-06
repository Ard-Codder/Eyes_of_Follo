import cv2 as cv
import numpy as np
import os

# Измените рабочую директорию на папку, в которой находится этот скрипт.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Можно использовать флаги IMREAD для различной предварительной обработки файлов изображений.
# Например, сделать их в оттенках серого или уменьшить размер.
# https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html - документация с параметрами
full_foto = cv.imread('foto_of_parking_many_white_cars.jpg', cv.IMREAD_UNCHANGED)
desired_object_foto = cv.imread('white_car_on_@foto_of_parking_many_white_cars@.jpg', cv.IMREAD_UNCHANGED)

# На выбор предлагается 6 методов сравнения(сопоставления):
# TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
# Различия можете увидеть с первого взгляда здесь:
# https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html
# Важно то, что значения инвертированы для TM_SQDIFF и TM_SQDIFF_NORMED.
result = cv.matchTemplate(full_foto, desired_object_foto, cv.TM_CCOEFF_NORMED)

# Результат matchTemplate() можно посмотреть следующим образом:
cv.imshow('Result', result)
cv.waitKey()

#  Я инвертировал порог и где сравнение для работаю с TM_SQDIFF_NORMED
threshold = 0.5

# Возвращаемое значение np.where() будет выглядеть следующим образом:
# (array([1, 2, 3, 4, 5], dtype=int32), array([11, 22, 33, 44, 55], dtype=int32))
locations = np.where(result >= threshold)

#  Мы можем заархивировать их в список кортежей позиций, типа (x, y)
locations = list(zip(*locations[::-1]))
print(locations)

count_of_objects = 0

if locations:
    print(f'Found object {count_of_objects}')

    needle_w = desired_object_foto.shape[1]
    needle_h = desired_object_foto.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4  # или любой пиксельный размер

    # Перебираем все локации и рисуем их прямоугольник
    for loc in locations:
        # Определяем позиции коробки
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        # Рисуем коробку
        cv.rectangle(full_foto, top_left, bottom_right, line_color, 2)

    cv.imshow('Matches', full_foto)
    cv.waitKey()
    # cv.imwrite('result.jpg', full_foto)

else:
    print('Needle not found.')
