import cv2 as cv
import numpy as np
import os

# Измените рабочую директорию на папку, в которой находится этот скрипт.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def find_click_positions(desired_object_foto_path, full_foto_path, threshold=0.5, debug_mode=None):
    # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
    full_foto = cv.imread(full_foto_path, cv.IMREAD_UNCHANGED)
    desired_object_foto = cv.imread(desired_object_foto_path, cv.IMREAD_UNCHANGED)
    # Сохраняем размеры изображения искомого объекта
    desired_object_foto_w = desired_object_foto.shape[1]
    desired_object_foto_h = desired_object_foto.shape[0]

    # На выбор предлагается 6 методов сравнения(сопоставления):
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(full_foto, desired_object_foto, method)

    # Получить все позиции из результата сопоставления, которые превышают наш порог
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    # print(locations)

    # Вы заметите, что нарисовано много перекрывающихся прямоугольников. Мы можем устранить эти лишние
    # местоположения с помощью groupRectangles().
    # Сначала нам нужно создать список прямоугольников, типа [x, y, w, h].
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), desired_object_foto_w, desired_object_foto_h]
        #  Добавляем каждый блок в список дважды, чтобы сохранить одиночные (неперекрывающиеся) блоки
        rectangles.append(rect)
        rectangles.append(rect)
    # Применение групповых прямоугольников.
    # Параметр groupThreshold обычно должен быть равен 1. Если вы поместите его в 0, группировка не будет выполняться.
    # Выполнено.
    # Если вы поставите его на 2, то для появления объекта требуется как минимум 3 перекрывающихся прямоугольника.
    # В результате я установил eps на 0,5, что составляет:
    # "Относительная разница между сторонами прямоугольников для объединения их в группу."
    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.2)
    # print(rectangles)

    points = []

    if len(rectangles):
        # print('Found object.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        # marker_type = cv.MARKER_STAR

        # Перебираем все прямоугольники
        for (x, y, w, h) in rectangles:

            # Определяем положение центра
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Сохраняем точку
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # Определяем позицию коробки
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Рисуем коробку
                cv.rectangle(full_foto, top_left, bottom_right, color=line_color,
                             lineType=line_type, thickness=2)
            elif debug_mode == 'cross':
                # Рисуем центральную точку
                cv.drawMarker(full_foto, (center_x, center_y),
                              color=marker_color, markerType=cv.MARKER_CROSS,
                              markerSize=30, thickness=2)

        if debug_mode:
            cv.imshow('Matches', full_foto)
            cv.waitKey()
            # cv.imwrite('result_click_point.jpg', haystack_img)

    return points


# Результат с использованием крестов
points = find_click_positions('white_car_on_@foto_of_parking_many_white_cars@.jpg',
                              'foto_of_parking_many_white_cars.jpg', debug_mode='cross', threshold=0.45)
print(points)

# Результат с использованием прямоугольников
points = find_click_positions('white_car_on_@foto_of_parking_many_white_cars@.jpg',
                              'foto_of_parking_many_white_cars.jpg',
                              threshold=0.45, debug_mode='rectangles')
print(points)
print('Done.')
