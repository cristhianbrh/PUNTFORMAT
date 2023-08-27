import pyautogui
from pynput.mouse import Listener

def get_color_at_mouse():
    x, y = pyautogui.position()
    colorPixel = pyautogui.pixel(x,y)

    r, g, b = colorPixel
    r = r /255
    g = g /255
    b = b /255

    print(r,g,b)
    # print(colorPixel)

def saveOnClick(x, y, button, pressed):
    if pressed and button == button.right:
        r,g,b = pyautogui.pixel(x,y)
        print(f'({r}/255,{g}/255,{b}/255)')
        
        exit_flag = True



def init_color_select():
    global exit_flag
    while not exit_flag:
        get_color_at_mouse()
        pyautogui.sleep(0.3)

        with Listener(on_click=saveOnClick) as listener:
            listener.join()
        
