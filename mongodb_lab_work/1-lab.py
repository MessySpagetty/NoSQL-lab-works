from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk
import json
from bson import json_util

def get_all_documents_projected():
    collection = db[cl_name]
    projection = {"type" : 1, "name" : 1}
    cursor = collection.find(projection = projection)
    i = 1
    for doc in cursor:
        documents_name[doc["_id"]] = f"{i}. Тип: {doc.get('type', 'неизвестный')}. Название: {doc.get('name', 'не определено')}"
        i += 1

    
def update_docs_combo():
    get_all_documents_projected()
    vals = [documents_name[k] for k in documents_name]
    docs_combo.configure(values=vals)
    

def show_documents():
    collection = db[cl_name]
    documents = list(collection.find())
    for doc in collection.find():
        doc_str = json_util.dumps(doc, indent=2, ensure_ascii=False)
        print(doc_str)
        docs_content_txt.insert(tk.END, doc_str + "\n------------------------------------\n")


def save_document():
    raise NotImplementedError

    
def insert_into_document_wrapper():
    doc_name = curr_doc.get()
    key = key_input.get()
    value = value_input.get()
    collection = db[cl_name]
    doc_id = None
    for k, v in documents_name.items():
        if v == doc_name:
            doc_id = k
            break
    if doc_id:
        insert_into_document(collection, doc_id, key, value)
        cur_pos = docs_combo.current()
        update_docs_combo()
        docs_combo.current(cur_pos)


def make_nested_dict(key, value):
    keys = key.split('.')
    last_key = keys[-1]
    nested_dict = {}
    current_level = nested_dict
    for k in keys[:-1]:
        current_level[k] = {}
        current_level = current_level[k]
    current_level[last_key] = value
    return nested_dict


def insert_into_document(collection, document_id, key, value):
    target = {"_id": document_id }
    collection.update_one(target, {'$set' : make_nested_dict(key, value)}, upsert=False)


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
string_to_display = tk.StringVar()

tk.Label(root, text="Текущий документ:").pack(pady=10)

docs_combo = ttk.Combobox(root, width=50, textvariable=curr_doc, state="readonly")
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

tk.Button(root, text="Добавить ключ-значение в текущий документ", command=insert_into_document_wrapper).pack(pady=10)

tk.Button(root, text="Сохранить документ", command=save_document).pack(pady=10)

tk.Button(root, text="Показать документы", command=show_documents).pack(pady=10)

docs_content_txt = tk.Text(root)
docs_content_txt.pack()


root.mainloop()