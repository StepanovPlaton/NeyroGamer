import pyvjoy
import pyautogui

def hello(): print("hello")

class СontrolClass():
    def __init__(self, NumberGamepad=1): 
        self.Gamepad = pyvjoy.VJoyDevice(1)
        self.Gamepad.reset()
    
    def SetLeftStick(self, X=0, Y=0):
        self.Gamepad.set_axis(pyvjoy.HID_USAGE_X, int((int(X*32767)/2)+16383))
        self.Gamepad.set_axis(pyvjoy.HID_USAGE_Y, 32767-int((int(Y*32767)/2)+16383))
    
    def SetButton(self, NumberButton, value):
        self.Gamepad.set_button(NumberButton, value)

    def PressKeyOnKeyboard(self, key):
        pyautogui.press(key)  