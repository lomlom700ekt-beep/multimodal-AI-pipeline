import pyautogui
import time
from datetime import datetime

def screenshot():
        today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")# strftime() — это метод, который превращает объект даты/времени в строку в заданном тобой формате.
        screenshot = pyautogui.screenshot()
        screenshot.save(f"C:/multimodal AI pipeline/screenshot/{today}.png")
        print(f"[{today}] Screenshot saved")
        return (f"C:/multimodal AI pipeline/screenshot/{today}.png"), today




