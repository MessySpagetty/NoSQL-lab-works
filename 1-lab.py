import redis
import tkinter.ttk as ttk
import tkinter as tk
import json

# Создание основного окна и установка его заголовка    
root = tk.Tk()
root.title("Настройки текстового сообщения")

SCR_WIDTH = root.winfo_screenwidth() 
SCR_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCR_WIDTH}x{SCR_HEIGHT}")

# Create a label
label = tk.Label(root, text="Текущий пользователь:")
label.pack(pady=10)

with open('user_settings.json', 'r') as file:
    user_settings = json.load(file)

choose_user_combo = ttk.Combobox(root, values=list(user_settings.keys()))
choose_user_combo.current(0)
choose_user_combo.pack()

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
