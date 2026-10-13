import sqlite3
from pathlib import Path
def database(data, today):
                application = data["application"]
                activity = data["activity"]
                connection = sqlite3.connect("activity.db")
                c = connection.cursor()
                c.execute(
                     "INSERT INTO activiti (time, application, activity) VALUES (?, ?, ?)",
                     (today, application, activity)
                )
                connection.commit()
                connection.close()


def bdrun(sql):
     db_path = Path(__file__).with_name("activity.db")
     db_uri = db_path.as_uri() + "?mode=ro"

    # Открываем базу только для чтения
     connection = sqlite3.connect(db_uri, uri=True)

     print(f"Выполнение запроса {sql} к базе sql.")
     try:
          sql = sql.strip()

          # Проверяем начало запроса
          first_word = sql.split(maxsplit=1)[0].upper() if sql else ""

          if first_word not in ("SELECT", "WITH"):
               raise ValueError("Разрешены только запросы чтения SELECT.")

          cursor = connection.cursor()

          # SQLite не позволит изменить базу в режиме read-only
          cursor.execute(sql)

          # Не забираем больше 500 строк
          result = cursor.fetchmany(500)

          return result

     finally:
          connection.close()