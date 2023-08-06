import pynput
import pyautogui


class CaptureRegionHelper:
    def __init__(self):
        self.first_click: bool = True
        self.top: int = 0
        self.left: int = 0
        self.bottom: int = 0
        self.right: int = 0
        self.listener = pynput.mouse.Listener(on_click=self.on_click)
        
    def start(self):
        print("Click top left corner of the capture region")
        self.listener.start()
        self.listener.join()
        self.standardize()
        height = self.bottom - self.top
        width = self.right - self.left
        return self.left, self.top, width, height
        
    def on_click(self, _x: int, _y: int, _button, pressed):
        if pressed:
            return
        # released
        x, y = pyautogui.position()
        print(f"x: {x}, y: {y}")
        if self.first_click:
            self.top = y
            self.left = x
            self.first_click = False
            print("Click bottom right corner of the capture region")
        else:
            self.bottom = y
            self.right = x
            return False
        
    def standardize(self):
        if self.top > self.bottom:
            self.top, self.bottom = self.bottom, self.top
        if self.left > self.right:
            self.left, self.right = self.right, self.left