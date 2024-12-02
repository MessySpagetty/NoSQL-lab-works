import redis
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import json

def cnvrt_to_tuple(rgb: str):
    return tuple(map(int, rgb.split()))


def get_hex(rgb: tuple):
    return "#%02x%02x%02x" % rgb  


def ask_color_handler():
    # получение цвета, выбранного пользователем в RGB формате 
    font_color.set(get_hex(colorchooser.askcolor()[0]))
    update_font()


def get_settings_values(user: str, var_name=None, index=None, mode=None):
    font_name.set(client.hget(MY_PREFIX + user, "font_name").decode("utf-8"))
    font_size.set(client.hget(MY_PREFIX + user, "font_size").decode("utf-8"))
    font_color.set(client.hget(MY_PREFIX + user, "font_color").decode("utf-8"))
    is_bold.set(client.hget(MY_PREFIX + user, "is_bold").decode("utf-8"))
    is_italic.set(client.hget(MY_PREFIX + user, "is_italic").decode("utf-8"))
    is_underline.set(client.hget(MY_PREFIX + user, "is_underline").decode("utf-8"))
    txt_entr.set(client.hget(MY_PREFIX + user, "example_text").decode("utf-8"))


def set_settings_values(user: str):
    client.hset(MY_PREFIX + user, "font_name", font_name.get())
    client.hset(MY_PREFIX + user, "font_size", font_size.get())
    client.hset(MY_PREFIX + user, "font_color", font_color.get())
    client.hset(MY_PREFIX + user, "is_bold", int(is_bold.get()))
    client.hset(MY_PREFIX + user, "is_italic", int(is_italic.get()))
    client.hset(MY_PREFIX + user, "is_underline", int(is_underline.get()))
    client.hset(MY_PREFIX + user, "example_text", txt_entr.get())


def change_user_wrapper():
    get_settings_values(current_user.get())
    update_font()


def update_font(var_name=None, index=None, mode=None):
    local_font_name = font_name.get()
    local_font_size = int(font_size.get()) if font_size.get() != "" else 12

    local_weight = "bold " if is_bold.get() else "normal "
    local_slant = "italic " if is_italic.get() else "roman "
    local_underline = "underline" if is_underline.get() else ""
    settings = local_weight + local_slant + local_underline

    rendered_txt.config(font=(local_font_name, local_font_size, settings.strip()), fg=font_color.get())


def save_settings_wrapper():
    set_settings_values(current_user.get())    


# Подключение к БД
with open('host', 'r') as file:
    HOST = file.read()
with open('passwd', 'r') as file:
    PASSWORD = file.read()
client = redis.StrictRedis(host=HOST, password=PASSWORD) 

# Префикс для уникальности ключей, чтобы совместно работать в БД
MY_PREFIX = "poskitt_22304_"

with open('user_settings.json', 'r') as file:
    user_settings_local = json.load(file)

# Загрузка локального файла с настройками в БД, в случае, если на БД настройки пользователей были сброшены
if client.get(MY_PREFIX + "is_set") is None:
    client.set(MY_PREFIX + "is_set", 1)
    for user in user_settings_local.keys():
        client.hset(MY_PREFIX + user, mapping=dict(user_settings_local[user]))

# Создание основного окна и установка его заголовка    
root = tk.Tk()
root.title("Настройки текстового сообщения")

SCR_WIDTH = root.winfo_screenwidth() 
SCR_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCR_WIDTH}x{SCR_HEIGHT}")

# Переменные для динамичского изменения настроек текста
current_user = tk.StringVar()
font_name = tk.StringVar()
font_size = tk.StringVar()
font_color = tk.StringVar()
is_bold = tk.BooleanVar()
is_italic = tk.BooleanVar()
is_underline = tk.BooleanVar()
txt_entr = tk.StringVar()

# Выбор пользователя
current_user_lbl = tk.Label(root, text="Текущий пользователь:")
current_user_lbl.pack(pady=10)

choose_user_combo = ttk.Combobox(root, values=list(user_settings_local.keys()), textvariable=current_user, state="readonly")
choose_user_combo.current(0)
choose_user_combo.pack()

settings_title_lbl = tk.Label(root, text="Задайте настройки для текущего пользователя:")
settings_title_lbl.pack()

# Выбор шрифта
settings_font_name_lbl = tk.Label(root, text="Шрифт:")
settings_font_name_lbl.pack()
settings_font_name_combo = ttk.Combobox(root, values=list(font.families()), textvariable=font_name, state="readonly")
settings_font_name_combo.current(0)
settings_font_name_combo.pack()

# Выбор размера текста
settings_font_size_lbl = tk.Label(root, text="Размер шрифта:")
settings_font_size_lbl.pack()
settings_font_size_entr = tk.Entry(root, textvariable=font_size)
settings_font_size_entr.pack()

# Выбор цвета текста
settings_font_color_clrchooser = tk.Button(root, text="Выбрать цвет", command=ask_color_handler)
settings_font_color_clrchooser.pack()

# Настройки начертания текста
settings_font_style_lbl = tk.Label(root, text="Начертание:")
settings_font_style_lbl.pack()

settings_font_bold_checkbox = tk.Checkbutton(root, text="Жирное", variable=is_bold, command=update_font)
settings_font_bold_checkbox.pack()

settings_font_italic_checkbox = tk.Checkbutton(root, text="Курсивное", variable=is_italic, command=update_font)
settings_font_italic_checkbox.pack()

settings_font_underline_checkbox = tk.Checkbutton(root, text="Подчёркнутое", variable=is_underline, command=update_font)
settings_font_underline_checkbox.pack()

# Исходная надпись
origin_txt_lbl = tk.Label(root, text="Исходная надпись:")
origin_txt_lbl.pack() 
origin_txt_entr = tk.Entry(root, textvariable=txt_entr)
origin_txt_entr.pack()

# Надпись с применёнными настройками
rendered_txt_lbl = tk.Label(root, text="Надпись с текущими настройками:")
rendered_txt_lbl.pack()
rendered_txt = tk.Label(root, textvariable=txt_entr, bg="white")
rendered_txt.pack()

# Кнопка для сохранения изменений
save_settings_btn = tk.Button(root, text="Сохранить изменения", command=save_settings_wrapper)
save_settings_btn.pack()

# Инициализация переменных перед отрисовкой окна и применение сохранённых изменений
current_user.set(list(user_settings_local.keys())[0])
get_settings_values(current_user.get())
update_font()

# Добавление обработчиков на событие изменения поля, так как label и combobox не поддерживают нативно параметр command
current_user.trace_add("write", lambda x, y, z: change_user_wrapper())
font_name.trace_add("write", update_font)
font_size.trace_add("write", update_font)

# Передача управления пользователю
root.mainloop()
