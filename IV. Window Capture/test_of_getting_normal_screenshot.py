# imports
import win32gui, win32con, ctypes
from PIL import ImageGrab
from ctypes import wintypes

# this takes care of the DPI settings (https://stackoverflow.com/questions/51786794/using-imagegrab-with-bbox-from-pywin32s-getwindowrect)
ctypes.windll.user32.SetProcessDPIAware()

# get window handle and dimensions
hwnd = win32gui.FindWindow(None, 'Steam')
dimensions = win32gui.GetWindowRect(hwnd)

# this gets the window size, comparing it to `dimensions` will show a difference
winsize = win32gui.GetClientRect(hwnd)

# this sets window to front if it is not already
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# grab screen region set in `dimensions`
image = ImageGrab.grab(dimensions)
image.show()

'''# we're going to use this to get window attributes
f = ctypes.windll.dwmapi.DwmGetWindowAttribute

# `rect` is for the window coordinates
rect = ctypes.wintypes.RECT()
DWMWA_EXTENDED_FRAME_BOUNDS = 9

# and then the coordinates of the window go into `rect`
f(ctypes.wintypes.HWND(hwnd),
  ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
  ctypes.byref(rect),
  ctypes.sizeof(rect)
  )

# if we want to work out the window size, for comparison this should be the same as `winsize`
size = (rect.right - rect.left, rect.bottom - rect.top)

# put the window coordinates in a tuple like that returned earlier by GetWindowRect()
dimensions = (rect.left, rect.top, rect.right, rect.bottom)
'''