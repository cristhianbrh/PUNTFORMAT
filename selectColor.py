import pyautogui

def get_color_at_mouse():
    x, y = pyautogui.position()
    colorPixel = pyautogui.pixel(x,y)

    r, g, b = colorPixel
    r = r /255
    g = g /255
    b = b /255
    print(r,g,b)
    print(colorPixel)


def init_color_select():
    while True:
        get_color_at_mouse()
        pyautogui.sleep(0.1)

