import redis
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import json

def ask_color_handler(event):
    # получение цвета, выбранного пользователем в RGB формате 
    font_color = colorchooser.askcolor()[0]

def update_font():
    default_font = font.nametofont("TkDefaultFont")
    local_font_name = font_name if font_name != "" else default_font.name
    local_font_size = int(font_size.get()) if font_size.get() != "" else 12
    custom_font = font.Font(family=local_font_name, size=local_font_size, weight="bold", slant="italic")
    return custom_font


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
font_size = tk.StringVar()
font_color = tuple
style_bold = tk.BooleanVar()
style_italic = tk.BooleanVar()
style_underline = tk.BooleanVar()
txt_entr = tk.StringVar()


choose_user_combo = ttk.Combobox(root, values=list(user_settings.keys()), textvariable=current_user)
choose_user_combo.current(0)
choose_user_combo.pack()


settings_title_lbl = tk.Label(root, text="Задайте настройки для текущего пользователя:")
settings_title_lbl.pack()

settings_font_name_lbl = tk.Label(root, text="Шрифт:")
settings_font_name_lbl.pack()
settings_font_name_combo = ttk.Combobox(root, values=list(font.families()), textvariable=font_name)
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

settings_font_bold_checkbox = tk.Checkbutton(root, text="Жирное", variable=style_bold)
settings_font_bold_checkbox.pack()

settings_font_italic_checkbox = tk.Checkbutton(root, text="Курсивное", variable=style_italic)
settings_font_italic_checkbox.pack()

settings_font_underline_checkbox = tk.Checkbutton(root, text="Подчёркнутое", variable=style_underline)
settings_font_underline_checkbox.pack()

# Надпись
origin_txt_lbl = tk.Label(root, text="Исходная надпись:")
origin_txt_lbl.pack()
origin_txt_entr = tk.Entry(root, textvariable=txt_entr)
origin_txt_entr.pack()

rendered_txt_lbl = tk.Label(root, text="Надпись с текущими настройками:")
rendered_txt_lbl.pack()
rendered_txt = tk.Label(root, textvariable=txt_entr, bg="white", font=update_font())
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
