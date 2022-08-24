import numpy as np
import win32gui
import win32ui
import win32con
import ctypes
from PIL import ImageGrab


class WindowCapture:
    # характеристики
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # конструктор
    def __init__(self, window_name):
        # найти "дескриптор" окна, которое мы хотим захватить
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window not found: {window_name}')

        # получаем размер окна
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # учитываем границу окна и заголовок и обрезаем их
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # устанавливаем смещение обрезанных координат, чтобы мы могли перевести скриншот
        # изображения в фактическое положение на экране
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):

        ctypes.windll.user32.SetProcessDPIAware()
        dimensions = win32gui.GetWindowRect(self.hwnd)

        # this gets the window size, comparing it to `dimensions` will show a difference
        winsize = win32gui.GetClientRect(self.hwnd)

        # this sets window to front if it is not already
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # grab screen region set in `dimensions`
        image = ImageGrab.grab(dimensions)

        '''# получить данные об изображении окна
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # преобразовать необработанные данные в формат, который может прочитать opencv
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signed_ints_array = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # свободные ресурсы
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # отключаем альфа-канал, иначе cv.matchTemplate() выдаст ошибку, например:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[..., :3]

        # сделать изображение C_CONTIGUOUS, чтобы избежать ошибок, которые выглядят следующим образом:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # см. обсуждение здесь:
        # https://github.com/opencv/opencv/issues/1486 6#issuecomment-580207109
        img = np.ascontiguousarray(img)'''

        return image

    # Найдем имя интересующего вас окна.
    # Как только вы это сделаете, обновите window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def win_enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(win_enum_handler, None)

    # Перевести положение пикселя на скриншоте в положение пикселя на экране.
    # поз = (х, у)
    # ПРЕДУПРЕЖДЕНИЕ: если вы переместите захватываемое окно после запуска выполнения, это
    # возвращаем неверные координаты, т.к. позиция окна вычисляется только в
    # конструктор __init__.
    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y


WindowCapture.list_window_names(1)
