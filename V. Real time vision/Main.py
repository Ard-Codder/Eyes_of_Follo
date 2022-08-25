import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision

# Измените рабочую директорию на папку, в которой находится этот скрипт.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# инициализируем класс WindowCapture
win_cap = WindowCapture('Steam')
# инициализируем класс Vision
vision_desired_object = Vision('Castle Crashers Icon.png')

'''
# https://www.crazygames.com/game/guns-and-bottle
wincap = WindowCapture()
vision_gunsnbottle = Vision('gunsnbottle.jpg')
'''

loop_time = time()
while True:

    # получить обновленный скрин игры
    screenshot = win_cap.get_screenshot()

    # сохраняем скрин в удобном виде для OpenCV
    image = np.array(screenshot)
    b, g, r = cv.split(image)

    # Изменили каналы, ибо появлялось не соответствие с оригинальным цветом
    merge_image = cv.merge([r, g, b])

    # отображаем обработанное изображение
    points = vision_desired_object.find(merge_image, 0.5, 'rectangles')
    # points = vision_desired_object.find(screenshot, 0.7, 'points')

    # отладка скорости цикла
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # Нажмите «Esc», когда окно вывода сфокусировано, чтобы выйти.
    # Цикл ждет каждые 1 мс для обработки нажатий клавиш
    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break

print('Done.')
