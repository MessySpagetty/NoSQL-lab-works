import redis
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import json


def get_hex(rgb):
    return "#%02x%02x%02x" % rgb  

def ask_color_handler():
    global font_color
    # получение цвета, выбранного пользователем в RGB формате 
    font_color = get_hex(colorchooser.askcolor()[0])
    update_font()

def update_font(*args):
    local_font_name = font_name.get()

    font_size_cur = font_size.get()
    local_font_size = int(font_size_cur) if font_size_cur != "" else 12

    settings = ""
    local_weight = "bold " if style_bold.get() else "normal "
    settings += local_weight

    local_slant = "italic " if style_italic.get() else "roman "
    settings += local_slant
    
    local_underline = "underline" if style_underline.get() else ""
    settings += local_underline

    rendered_txt.config(font=(local_font_name, local_font_size, settings.strip()), fg=font_color)


# Создание основного окна и установка его заголовка    
root = tk.Tk()
root.title("Настройки текстового сообщения")

SCR_WIDTH = root.winfo_screenwidth() 
SCR_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCR_WIDTH}x{SCR_HEIGHT}")

# Create a label
current_user_lbl = tk.Label(root, text="Текущий пользователь:")
current_user_lbl.pack(pady=10)

with open('user_settings.json', 'r') as file:
    user_settings = json.load(file)

current_user = tk.StringVar()
font_name = tk.StringVar()
font_name.trace_add("write", update_font)
font_size = tk.StringVar()
font_size.trace_add("write", update_font)
global font_color
font_color = "black"
style_bold = tk.BooleanVar()
style_italic = tk.BooleanVar()
style_underline = tk.BooleanVar()
txt_entr = tk.StringVar()


choose_user_combo = ttk.Combobox(root, values=list(user_settings.keys()), textvariable=current_user, state="readonly")
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

settings_font_bold_checkbox = tk.Checkbutton(root, text="Жирное", variable=style_bold, command=update_font)
settings_font_bold_checkbox.pack()

settings_font_italic_checkbox = tk.Checkbutton(root, text="Курсивное", variable=style_italic, command=update_font)
settings_font_italic_checkbox.pack()

settings_font_underline_checkbox = tk.Checkbutton(root, text="Подчёркнутое", variable=style_underline, command=update_font)
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

# Передача управления пользователю
root.mainloop()

# region подключение к БД

# with open('host', 'r') as file:
#     HOST = file.read()  # Reads the entire file

# with open('passwd', 'r') as file:
#     PASSWORD = file.read()

# client = redis.StrictRedis(host=HOST, password=PASSWORD)

# # Префикс для уникальности ключей, чтобы совместно работать в БД
# my_prefix = "poskitt_22304_"

# # Set a key-value pair
# client.set(my_prefix + 'my_key', 'Hello, Redis!')

# # Retrieve the value
# value = client.get(my_prefix + 'my_key')

# print(value.decode('utf-8'))  # Output: Hello, Redis!

# endregion 
