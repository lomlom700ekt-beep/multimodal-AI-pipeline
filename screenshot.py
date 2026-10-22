import io
import base64

import pyautogui
from datetime import datetime


def screenshot():
        """Делает скриншот экрана и возвращает его в виде base64-строки без сохранения на диск.

        :return: (image_base64, today) - изображение в формате base64 и метка времени.
        """
        today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")# strftime() — это метод, который превращает объект даты/времени в строку в заданном тобой формате.
        image = pyautogui.screenshot()

        # Кодируем PNG в памяти, файлы на диск не создаются
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        print(f"[{today}] Screenshot captured in memory ({len(image_base64)} base64 chars)")
        return image_base64, today

