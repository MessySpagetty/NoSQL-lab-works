from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk
import json


def get_team_documents(collection):
    query = {'type': 'Команда'}
    projection = {'team_name': 1}
    cursor = collection.find(query, projection)
    for doc in cursor:
        documents_name[doc["_id"]] = f"Команда: {doc.get('team_name', 'Неизвестно')}"


def get_game_documents(collection):
    query = {'type': 'Матч'}
    projection = {'date_of_match': 1}
    cursor = collection.find(query, projection)
    for doc in cursor:
        documents_name[doc["_id"]] = f"Матч: {doc.get('date_of_match', 'Неизвестно')}"


def get_undefined_documents(collection):
    query = {
        "type": {
            "$nin": ["Матч", "Команда"]
        }
    }
    cursor = collection.find(query)
    for doc in cursor:
        documents_name[doc["_id"]] = f"Тип: {doc.get('type', 'неизвестный')}, id: {doc['_id']}"


def get_all_documents():
    collection = db[cl_name]
    get_game_documents(collection)  
    get_team_documents(collection)
    get_undefined_documents(collection)

    
def update_docs_combo():
    get_all_documents()
    vals = [documents_name[k] for k in documents_name]
    docs_combo.configure(values=vals)
    

def show_documents():
    raise NotImplementedError


def save_document():
    raise NotImplementedError


def insert_into_document_wrapper():
    doc_name = curr_doc.get()
    k = key_input.get()
    v = value_input.get()
    collection = db[cl_name]
    insert_into_document(collection, doc_id, k, v)
    update_docs_combo()


def insert_into_document(collection, document_id, key, value):
    target = { f"_id = { document_id }" }
    new_doc = { f"{key} : {value}" }
    collection.insert_one(target, new_doc)


def create_document():
    inp = document_name_input.get()
    tp = "Неизвестный" if inp == "" else inp  
    db[cl_name].insert_one({"type": tp})
    update_docs_combo()

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

# Словарь для отображения документов
documents_name = { }
 
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

docs_combo = ttk.Combobox(root, width=35, textvariable=curr_doc, state="readonly")
update_docs_combo()
docs_combo.current(0)
docs_combo.pack()

options = ("Матч", "Команда")
ttk.Combobox(root, textvariable=document_name_input, values=options, state="readonly").pack(pady=10)
tk.Button(root, text="Создать ещё документ", command=create_document).pack(pady=10)

tk.Label(root, text="Ключ или вложенные ключи (через точку):").pack()
tk.Entry(root, textvariable=key_input).pack()

tk.Label(root, text="Значение:").pack()
tk.Entry(root, textvariable=value_input).pack()

tk.Button(root, text="Добавить ключ-значение в текущий документ", command=insert_into_document).pack(pady=10)

tk.Button(root, text="Сохранить документ", command=save_document).pack(pady=10)

tk.Button(root, text="Показать документы", command=show_documents).pack(pady=10)

root.mainloop()