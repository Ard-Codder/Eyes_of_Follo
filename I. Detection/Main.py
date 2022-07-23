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
# Если вы хотите сохранить этот результат в файл, вам необходимо нормализовать массив результатов.
# Из 0..1 в 0..255, ссылка:
# https://stackoverflow.com/questions/35719480/opencv-black-image-after-matchtemplate
# cv.imwrite('result_CCOEFF_NORMED.jpg', result * 255)

# Получение лучшей позиции в совпадения по результату сопоставления.
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
# Максимальное местоположение будет содержать положение пикселя в верхнем левом углу области,
# который наиболее точно соответствует нашему изображению искомого объекта. Максимальное значение дает указание
# того, насколько эта находка похожа на искомый объект, где 1 идеально и -1 не подходит.
print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

# Если значение наилучшего совпадения больше threshold, мы будем полагать, что нашли совпадение.
threshold = 0.8
if max_val >= threshold:
    print('Found desired object.')

    # Получите размер изображения искомого объекта. С помощью функций изображения в OpenCV вы можете получить размеры
    # через свойство формы. Он возвращает кортеж количества строк, столбцов и каналы (если изображение цветное):
    desired_object_w = desired_object_foto.shape[1]
    desired_object_h = desired_object_foto.shape[0]

    # Вычисляем нижний правый угол прямоугольника, чтобы нарисовать
    top_left = max_loc
    bottom_right = (top_left[0] + desired_object_w, top_left[1] + desired_object_h)

    # Рисуем прямоугольник на нашем снимке экрана, чтобы выделить место, где мы нашли искомый объект.
    # Цвет линии может быть установлен как кортеж RGB
    cv.rectangle(full_foto, top_left, bottom_right,
                 color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    # Вы можете просмотреть обработанный снимок экрана следующим образом:
    cv.imshow('Result', full_foto)
    cv.waitKey()
    # Или вы можете сохранить результаты в файл.
    # imwrite() будет разумно форматировать наше выходное изображение на основе расширения, которое мы ему даем
    # https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
    cv.imwrite('result.jpg', full_foto)

else:
    print('Desired object not found.')
