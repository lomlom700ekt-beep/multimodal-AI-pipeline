from screenshot import screenshot
import requests
import base64
import json
from sqlbd import database
import time
from ask_llm_lmstudio import ask_model
time.sleep(5) 
def main():
            # 1. Делаем скриншот
            file, today = screenshot()


            # 2. Читаем изображение и переводим его в Base64
            with open(file, "rb") as image_file: # read binary → «открыть файл для чтения как бинарные данные»
                image_base64 = base64.b64encode(image_file.read()).decode("utf-8")


            # 3.prompt
            prompt = """
            Проанализируй скриншот как одну запись в журнале активности пользователя.

            Верни ТОЛЬКО JSON следующего формата:

            {
            "application": "название основного приложения или сайта",
            "activity": "что пользователь делает, 5-10 слов"
            }

            Правила:

            * application — только название приложения или сайта.
            * Не добавляй в application время, дату, описание действий или дополнительный контекст.
            * Например: "VS Code", "Google Chrome", "Диспетчер задач", "Discord".
            * activity — кратко опиши основное действие пользователя, 5-10 слов.
            * Не перечисляй элементы интерфейса, системные показатели, цвета, расположение элементов и другие несущественные детали.
            * Не переписывай текст со скриншота.
            * Не делай предположений, которых нельзя подтвердить по изображению.
            * Если приложение или действие неизвестны, используй "unknown".
            * Будь максимально кратким.
            """

            model = "gemma-4-e4b-uncensored-hauhaucs-aggressive-hf"
            # 4. Формируем запрос для LM Studio
            model_output = ask_model(model,prompt,image_base64,)
            data = json.loads(model_output)

            return data, today
while True:
    data, today =  main()

    database(data, today)
    time.sleep(300) 
