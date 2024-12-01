import redis
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import json


def update_tree(leaderboard, tree):
    for row in tree.get_children():
        tree.delete(row)

    for sp in leaderboard:
        tree.insert("", "end", values=sp)


def get_leaderboard(judges):
    judges = [MY_PREFIX + ju for ju in judges]
    client.zunionstore(MY_PREFIX + "leaderboard", judges, aggregate="sum")
    return client.zrange(MY_PREFIX + "leaderboard", 0, -1, desc=True, withscores=True)


def update_leaderboard(judge, sportsman, score):
    client.zincrby(MY_PREFIX + judge, score, sportsman)


def save_results(judge, sportsman, score, tree):
    update_leaderboard(judge, sportsman, score)
    leaderboard = get_leaderboard(judges)
    decoded_leaderboard = ((sp[0].decode('utf-8'), int(sp[1])) for sp in leaderboard)
    update_tree(decoded_leaderboard, tree)


def save_results_wrapper():
    j = curr_judge.get()
    sp = curr_sportsman.get()
    sc = given_score.get()
    save_results(j, sp, sc, rating_tree)


def init_leaderbord(judges, sportsmans):
    # Три таблицы, по одной на каждого судью. В каждой таблице хранятся отсортированные множества -- 
    # спортсмены и выставленные им этим судьёй баллы
    for ju in judges:
        client.zadd(MY_PREFIX + ju, mapping=sportsmans)


def init_tree(sportsmans):
    columns = ("Surname", "Score")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("Surname", text="Фамилия")
    tree.heading("Score", text="Сумма баллов")
    for sp in sportsmans.keys():
        tree.insert("", "end", values=(sp, sportsmans[sp]))
    return tree


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

# Список судей и спортсменов соответственно
judges = ("Mr. Red", "Mr. Green", "Mr. Blue")
sportsmans = {"Faster": 0, "Higher": 0, "Stronger": 0}

# Выбор судьи
judge_lbl = tk.Label(root, text="Судья:").pack(pady=10)

judge_combo = ttk.Combobox(root, values=judges, textvariable=curr_judge, state="readonly")
judge_combo.current(0)
judge_combo.pack()

# Выбор спортсмена
sportsman_lbl = tk.Label(root, text="Спортсмен:").pack(pady=10)

sportsman_combo = ttk.Combobox(root, values=list(sportsmans.keys()), textvariable=curr_sportsman, state="readonly")
sportsman_combo.current(0)
sportsman_combo.pack()

# Выставление баллов
sportsman_lbl = tk.Label(root, text="Выставить баллы:").pack(pady=10)

score_entry = tk.Entry(root, textvariable=given_score)
score_entry.pack()

# Сохранение выставленного балла
save_score = tk.Button(root, text="Сохранить", command=save_results_wrapper)
save_score.pack(pady=10)

# Рейтинг-лист
rating_tree = init_tree(sportsmans)
rating_tree.pack()

init_leaderbord(judges, sportsmans)

# Передача управления пользователю
root.mainloop()
