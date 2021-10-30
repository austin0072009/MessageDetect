import numpy as np
import cv2 as cv
import pyautogui

class Window_Capture:


    def __init__(self,target,threshold):
        self.target= target
        self.threshold= threshold

    def getScreenshot(self):
        screenshot= pyautogui.screenshot()
        screenshot= np.array(screenshot)
        screenshot= cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)

        result = cv.matchTemplate(screenshot, self.target, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val >= self.threshold:
            return 1
        else:
            return 0

