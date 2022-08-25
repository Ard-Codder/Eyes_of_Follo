import cv2 as cv
import numpy as np


class Vision:
    # характеристики
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # конструктор
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # загрузить изображение, которое мы пытаемся сопоставить
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        # Сохраните размеры искомого объекта
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # На выбор предлагается 6 методов:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5, debug_mode=None):
        # запустить алгоритм OpenCV
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Получить все позиции из результатов матча, которые превышают наш порог
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # Вы заметите, что нарисовано много перекрывающихся прямоугольников. Мы можем устранить эти лишние
        # места с помощью groupRectangles().
        # Сначала нам нужно создать список прямоугольников [x, y, w, h]
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Добавьте каждое поле в список дважды, чтобы сохранить одиночные (неперекрывающиеся) поля.
            rectangles.append(rect)
            rectangles.append(rect)
        # Примените групповые прямоугольники.
        # Параметр groupThreshold обычно должен быть равен 1.
        # Если вы поместите его в 0, группировка не будет выполняться.
        # Выполнено. Если вы поставите его на 2,
        # то для появления объекта требуется как минимум 3 перекрывающихся прямоугольника.
        # В результате. Я установил eps на 0,5, что составляет:
        # «Относительная разница между сторонами прямоугольников, чтобы объединить их в группу».
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        # print(rectangles)

        points = []
        if len(rectangles):
            # print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Перебрать все прямоугольники
            for (x, y, w, h) in rectangles:

                # Определяем положение центра
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                # Сохраняем позиции
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    # Определяем положение коробки
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Рисуем коробку
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                                 lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Рисуем центральную точку
                    cv.drawMarker(haystack_img, (center_x, center_y),
                                  color=marker_color, markerType=marker_type,
                                  markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)
            # cv.waitKey()
            # cv.imwrite('result_click_point.jpg', haystack_img)

        return points
