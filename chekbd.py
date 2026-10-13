import sqlite3
connection = sqlite3.connect("activity.db")# создание или открытие базы activity.db

cursor = connection.cursor()

cursor.execute("SELECT * FROM activiti")# выборка всех данных из таблицы activiti
print(cursor.fetchall()) # .fetchall() получить все записи которые были выбранны выше 
connection.commit()# сохранить обновить бд, сделать коммит 
connection.close()