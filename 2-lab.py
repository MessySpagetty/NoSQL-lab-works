import redis
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import json

# Подключение к БД
with open('host', 'r') as file:
    HOST = file.read()
with open('passwd', 'r') as file:
    PASSWORD = file.read()
client = redis.StrictRedis(host=HOST, password=PASSWORD) 

# Префикс для уникальности ключей, чтобы совместно работать в БД
MY_PREFIX = "poskitt_22304_"

# Создание основного окна и установка его заголовка    
root = tk.Tk()
root.title("Монитор спортивных соревнований")

SCR_WIDTH = root.winfo_screenwidth() 
SCR_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCR_WIDTH}x{SCR_HEIGHT}")

# Переменные для динамичского изменения настроек текста
curr_judge = tk.StringVar()
curr_sportsman = tk.StringVar()
given_score = tk.StringVar()

# Выбор судьи
judge_lbl = tk.Label(root, text="Судья:").pack(pady=10)

judge_combo = ttk.Combobox(root, values=list(user_settings_local.keys()), textvariable=curr_judge, state="readonly")
judge_combo.current(0)
judge_combo.pack()

# Выбор спортсмена
sportsman_lbl = tk.Label(root, text="Спортсмен:").pack(pady=10)

sportsman_combo = ttk.Combobox(root, values=list(user_settings_local.keys()), textvariable=curr_sportsman, state="readonly")
sportsman_combo.current(0)
sportsman_combo.pack()

# Выставление баллов
sportsman_lbl = tk.Label(root, text="Выставить баллы:").pack(pady=10)

score_entry = tk.Entry(root, textvariable=given_score)

# Передача управления пользователю
root.mainloop()
