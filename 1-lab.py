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

def get_color_from_redis_in_hex(user: str):
    color_from_redis = (client.hget(MY_PREFIX + user, "font_color")).decode('utf-8')
    return get_hex(cnvrt_to_tuple(color_from_redis))

def get_settings_values(user: str):
    font_name.set(client.hget(MY_PREFIX + user, "font_name").decode("utf-8"))
    font_size.set(client.hget(MY_PREFIX + user, "font_size").decode("utf-8"))
    font_color.set(get_color_from_redis_in_hex(user))
    is_bold.set(client.hget(MY_PREFIX + user, "is_bold").decode("utf-8"))
    is_italic.set(client.hget(MY_PREFIX + user, "is_italic").decode("utf-8"))
    is_underline.set(client.hget(MY_PREFIX + user, "is_underline").decode("utf-8"))
    txt_entr.set(client.hget(MY_PREFIX + user, "example_text").decode("utf-8"))


def ask_color_handler():
    # получение цвета, выбранного пользователем в RGB формате 
    font_color.set(get_hex(colorchooser.askcolor()[0]))
    update_font()


def update_font(*args):
    local_font_name = font_name.get()

    font_size_cur = font_size.get()
    local_font_size = int(font_size_cur) if font_size_cur != "" else 12

    settings = ""
    local_weight = "bold " if is_bold.get() else "normal "
    settings += local_weight

    local_slant = "italic " if is_italic.get() else "roman "
    settings += local_slant
    
    local_underline = "underline" if is_underline.get() else ""
    settings += local_underline

    rendered_txt.config(font=(local_font_name, local_font_size, settings.strip()), fg=font_color.get())


def key_have_expired(key):
    value = client.get(MY_PREFIX + key)
    return value == None


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

# Инициализация переменных перед отрисовкой окна
current_user.set(list(user_settings_local.keys())[0])
get_settings_values(current_user.get())

# Create a label
current_user_lbl = tk.Label(root, text="Текущий пользователь:")
current_user_lbl.pack(pady=10)

choose_user_combo = ttk.Combobox(root, values=list(user_settings_local.keys()), textvariable=current_user, state="readonly")
choose_user_combo.current(0)
choose_user_combo.pack()


settings_title_lbl = tk.Label(root, text="Задайте настройки для текущего пользователя:")
settings_title_lbl.pack()

settings_font_name_lbl = tk.Label(root, text="Шрифт:")
settings_font_name_lbl.pack()
settings_font_name_combo = ttk.Combobox(root, values=list(font.families()), textvariable=font_name, state="readonly")
settings_font_name_combo.current(0)
settings_font_name_combo.pack()

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

# Надпись
origin_txt_lbl = tk.Label(root, text="Исходная надпись:")
origin_txt_lbl.pack() 
origin_txt_entr = tk.Entry(root, textvariable=txt_entr)
origin_txt_entr.pack()

rendered_txt_lbl = tk.Label(root, text="Надпись с текущими настройками:")
rendered_txt_lbl.pack()
rendered_txt = tk.Label(root, textvariable=txt_entr, bg="white")
rendered_txt.pack()

# Добавление обработчиков на событие изменения поля
font_name.trace_add("write", update_font)
font_size.trace_add("write", update_font)

# Передача управления пользователю
root.mainloop()
