from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk
import json


def get_team_documents(collection):
    query = {'type': 'Команда'}
    projection = {'team_name': 1, '_id': 0}
    teams = [f"Команда: {doc['team_name']}" for doc in collection.find(query, projection)]
    return teams


def get_game_documents(collection):
    query = {'type': 'Игра'}
    projection = {'date_of_match': 1, 'type': 1, '_id': 0}
    games = [f"Игра: {doc['date_of_match']}" for doc in collection.find(query, projection)]
    return games


def get_team_and_game_documents():
    collection = db[cl_name]
    return get_game_documents(collection) + get_team_documents(collection)


def show_documents():
    raise NotImplementedError


def save_document():
    raise NotImplementedError


def insert_into_document_wrapper():
    doc_name = curr_doc.get()
    insert_into_document(doc_name)


def insert_into_document():
    raise NotImplementedError


def create_document():
    coll_name = document_name_input.get()
    if coll_name:
        db.create_collection(coll_name)
        docs_combo.configure(values=get_team_documents(coll_name))


# Подключение к БД
port="22304"
uri=f'mongodb://localhost:{port}'
db_name = '1-lab-db'

client = MongoClient(uri)
db = client[db_name]

# Инициализация коллекций
for coll in db.list_collection_names():
    db[coll].drop()

cl_name = "football_teams_and_mathes"
db.create_collection(cl_name, check_exists=False)

collection = db[cl_name]

with open('teams_and_matches.json', 'r', encoding='utf-8') as json_file:
    db[cl_name].insert_many(json.load(json_file))

# Создание основного окна и установка его заголовка    
root = tk.Tk()
root.title("Информация о футбольных командах")

SCR_WIDTH = root.winfo_screenwidth() 
SCR_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCR_WIDTH}x{SCR_HEIGHT}")

curr_doc = tk.StringVar()
document_name_input = tk.StringVar()
key_input = tk.StringVar()
value_input = tk.StringVar()

curr_doc_content = ""

tk.Label(root, text="Текущий документ:").pack(pady=10)

docs_combo = ttk.Combobox(root, width=35, values=get_team_and_game_documents(), textvariable=curr_doc, state="readonly")
docs_combo.current(0)
docs_combo.pack()


tk.Entry(textvariable=document_name_input).pack(pady=10)
tk.Button(root, text="Создать ещё документ", command=create_document).pack(pady=10)

tk.Label(root, text="Ключ или вложенные ключи (через точку):").pack()
tk.Entry(root, textvariable=key_input).pack()

tk.Label(root, text="Значение:").pack()
tk.Entry(root, textvariable=key_input).pack()

tk.Button(root, text="Добавить ключ-значение в текущий документ", command=insert_into_document).pack(pady=10)

tk.Button(root, text="Сохранить документ", command=save_document).pack(pady=10)

tk.Button(root, text="Показать документы", command=show_documents).pack(pady=10)

root.mainloop()