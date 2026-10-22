import sqlite3
from ask_llm_lmstudio import ask_model
import json
from datetime import datetime

def chek_code_sql(code, user_query, db_schema, max_attempts):
    model = "gemma-4-e4b-uncensored-hauhaucs-aggressive-hf"
    current_sql = code

    # Открываем базу только для чтения
    connection = sqlite3.connect(
        "file:activity.db?mode=ro",
        uri=True
    )
    try:
        for attempt in range(max_attempts):
            try:
                cursor = connection.cursor()
                cursor.execute(current_sql)

                # SQL выполнился без ошибки
                print("SQL успешно выполнен!")
                return current_sql

            except sqlite3.Error as e:
                sql_error = str(e)

                print(
                    f"Попытка {attempt + 1}/{max_attempts}: "
                    f"ошибка SQL: {sql_error}"
                )

                # Если попытки закончились, дальше не обращаемся к LLM
                if attempt == max_attempts - 1:
                    break
                dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                prompt = f"""
Ты — помощник по исправлению SQL-запросов для SQLite.

Текущее время: {dt}

Вопрос пользователя:
{user_query}

Последний SQL-запрос:
{current_sql}

Реальная ошибка SQLite:
{sql_error}

Структура базы данных:
{db_schema}

Исправь SQL так, чтобы он выполнялся в SQLite
и отвечал на исходный вопрос пользователя.

Правила:
- Сохраняй смысл исходного вопроса.
- Используй только существующие таблицы и столбцы.
- Исправляй причину ошибки, а не просто маскируй её.
- Не выдумывай данные и названия столбцов.
- Создавай только запрос чтения данных.
- Разрешены SELECT и WITH, который выполняет SELECT.
- Не выполняй запрос самостоятельно.
- Если исправить запрос невозможно, верни пустую строку
  в поле sql и объясни причину в поле error.

Верни только JSON:
{{
    "sql": "исправленный SQL-запрос",
    "error": ""
}}
"""

                model_output = ask_model(
                    model=model,
                    prompt=prompt
                )

                try:
                    # Убираем Markdown-обрамление, если модель его добавила
                    model_output = model_output.strip()

                    if model_output.startswith("```"):
                        model_output = model_output.split("\n", 1)[1]
                        model_output = model_output.rsplit("```", 1)[0]

                    result = json.loads(model_output.strip())

                except (json.JSONDecodeError, AttributeError, IndexError):
                    print("Модель вернула некорректный JSON.")
                    break

                new_sql = result.get("sql", "").strip()
                model_error = result.get("error", "").strip()

                if not new_sql:
                    print("Модель не смогла исправить SQL:", model_error)
                    break

                # Следующая попытка проверит уже исправленный SQL
                current_sql = new_sql

        print("Не удалось получить рабочий SQL.")
        return None

    finally:
        connection.close()

