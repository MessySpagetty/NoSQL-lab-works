import redis
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
import json

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

choose_user_combo = ttk.Combobox(root, values=list(user_settings.keys()))
choose_user_combo.current(0)
choose_user_combo.pack()

settings_title_lbl = tk.Label(root, text="Задайте настройки для текущего пользователя:")
settings_title_lbl.pack()

settings_font_name_lbl = tk.Label(root, text="Шрифт:")
settings_font_name_lbl.pack()
settings_font_name_combo = ttk.Combobox(root, values=list(font.families()))
settings_font_name_combo.pack()

settings_font_size_lbl = tk.Label(root, text="Размер шрифта:")
settings_font_size_lbl.pack()
settings_font_size_entr = tk.Entry(root)
settings_font_size_entr.pack()

# Настройки начертания текста
settings_font_style_lbl = tk.Label(root, text="Начертание:")
settings_font_style_lbl.pack()

bold_var = tk.BooleanVar()
settings_font_bold_checkbox = tk.Checkbutton(root, text="Bold", variable=bold_var)
italic_var = tk.BooleanVar()
settings_font_italic_checkbox = tk.Checkbutton(root, text="Italic", variable=italic_var)
underline_var = tk.BooleanVar()
settings_font_underline_checkbox = tk.Checkbutton(root, text="Underline", variable=underline_var)

settings_font_bold_checkbox.pack()
settings_font_italic_checkbox.pack()
settings_font_underline_checkbox.pack()








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
