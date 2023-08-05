import cv2
import win32gui, win32ui, win32con, win32api
from ctypes import windll
from PIL import Image, ImageGrab
import numpy as np
from mss import mss
from pynput.mouse import Button, Controller

def mouse_click(pos, button='left'):
    """
    pos: tuple(x,y)
    button: 'right' or 'middle' or 'left'
    """
    _mouse = Controller()
    _mouse.position = pos
    if button=='right': _mouse.click(Button.right)
    elif button=='middle': _mouse.click(Button.middle)
    elif button=='left': _mouse.click(Button.left)

def imread_hangul(path):
    img_array = np.fromfile(path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def get_capture_image(bbox=None):
    """
    Capture a screenshot of the specified area or the entire screen.

    :param bbox: A tuple specifying the area to capture (left, top, right, bottom).
                 If None, capture the entire screen.
    :return: The captured screenshot as a PIL.Image.
    """
    if bbox:
        if not isinstance(bbox, tuple) or len(bbox) != 4:
            raise ValueError("input type: tuple(left, top, right, bottom)")
        ss_img = ImageGrab.grab(bbox)
    else:
        ss_img = ImageGrab.grab(all_screens=True)
    return ss_img


def get_capture_image_with_save(bbox=None, filename="capture.jpg"):
    """
    Capture a screenshot of the specified area or the entire screen.

    :param bbox: A tuple specifying the area to capture (left, top, right, bottom).
                 If None, capture the entire screen.
    :param filename: The name of the file where the screenshot will be saved.
    :return: The captured screenshot as a PIL.Image.
    """
    ss_img = get_capture_image(bbox)
    ss_img.save(filename)
    return ss_img


class MatchProcess():

    def __init__(self, large_image, small_image):
        try: self.large_image = imread_hangul(large_image) # Read the images from the file
        except: self.large_image = large_image
        try: self.small_image = imread_hangul(small_image) # Read the images from the file
        except: self.small_image = small_image

        method = cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(self.small_image, self.large_image, method)
        self.mn, _, self.mnLoc, _ = cv2.minMaxLoc(result)  # min_val, max_val, min_loc, max_loc
        self.MPx, self.MPy = self.mnLoc
        self.trows, self.tcols = self.small_image.shape[:2]

    def get_accuracy(self):
        return (1.0 - self.mn)

    def draw_rect(self):
        cv2.rectangle(self.large_image, (self.MPx, self.MPy), (self.MPx + self.tcols, self.MPy + self.trows), (0, 0, 255), 2)
        cv2.imwrite('match.png', self.large_image)  # cv2.imshow('match',large_image), cv2.waitKey(0)

    def value(self):  # center_pos, xywh, min_value
        return (int(self.MPx + self.tcols / 2), int(self.MPy + self.trows / 2)), (self.MPx, self.MPy, self.trows, self.tcols), (1.0 - self.mn)

def match_image_check(large_image, small_image, dest_acc=0.98):
    """
    Compare two images and check if they match based on a given accuracy criterion.

    :param large_image: The larger image to be compared.
    :param small_image: The smaller image to be compared.
    :param dest_acc: The minimum accuracy for the images to be considered a match.
    :return: If the images match, returns a tuple containing center position, 
             dimensions, and the accuracy score. Otherwise, returns a tuple 
             with (-1, -1) for the position and the accuracy score.
    """
    mp = MatchProcess(large_image, small_image)
    acc = mp.get_accuracy()
    if dest_acc < acc:
        return mp.value()
    else:
        return (-1, -1, acc)


def match_with_image_write(large_image, small_image, dest_acc=0.98):
    """
    Compare two images and check if they match based on a given accuracy criterion.
    If the images match, it also saves the result as 'match.png'.

    :param large_image: The larger image to be compared.
    :param small_image: The smaller image to be compared.
    :param dest_acc: The minimum accuracy for the images to be considered a match.
    :return: If the images match, returns a tuple containing center position, 
             dimensions, and the accuracy score, and saves the result as 'match.png'. 
             Otherwise, returns a tuple with (-1, -1) for the position and the accuracy score.
    """
    mp = MatchProcess(large_image, small_image)
    acc = mp.get_accuracy()
    if dest_acc < acc:
        mp.draw_rect()
        return mp.value()
    else:
        return (-1, -1, acc)


def cv2_to_pil(cv_image):
    img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    return im_pil


def pil_to_cv2(pil_image):
    open_cv_image = np.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    return open_cv_image


def get_capture_image_on_app(win_name):
    """
    :param win_name: detect window from name
    return: cv2 window screenshot
    """
    try:
        hwnd = win32gui.FindWindowEx(None, None, None, win_name)  # maplestory
    except:
        try:
            hwnd = win32gui.FindWindow(None, win_name)
        except:
            raise ("can't get hwnd")
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)

    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        return pil_to_cv2(im)


def test_screen(app_name="MapleStory",left=0, top=0, width=300, height=300):
    while True:
        cv2.imshow('screen', get_capture_image_on_app(app_name))
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


def app_click(win_name, x, y):
    hwnd = win32gui.FindWindow(None, win_name)
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, None)

    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd1, win32con.WM_LBUTTONUP, None, lParam)
