import cv2 as cv
import os
from time import time

import numpy as np

from windowcapture import WindowCapture

# Измените рабочую директорию на папку, в которой находится этот скрипт.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# инициализируем класс WindowCapture

# EYES_OF_FOLLO – Main.py
wincap = WindowCapture('Discord')

loop_time = time()
while True:

    # получить обновленный скрин игры(приложения)
    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', np.array(screenshot))

    # отладка скорости цикла
    print(f'FPS {1 / (time() - loop_time)}')
    loop_time = time()

    # Нажмите 'Esc', когда окно вывода сфокусировано, чтобы выйти.
    # Ждет 1 мс в каждом цикле для обработки нажатия клавиш
    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break

print('Done.')
