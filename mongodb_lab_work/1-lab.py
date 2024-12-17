from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk
import json
from bson import json_util


def show_commands_with_cards():
    
    pipeline = [
        {
            '$unwind': '$teams'
        },
        {
            '$unwind': '$yellow-red-cards'
        },
        {
            '$group': {
                '_id': '$teams.team_name', 
                'total_yellow_red_cards': { '$sum': 1 }
            }
        },
        {
            '$sort': { 'total_yellow_red_cards': -1 }
        },
        {
            '$limit': 1
        },
        {
            '$project': {
                'team_name': '$_id',
                'total_yellow_red_cards': 1,
                '_id': 0
            }
        }
    ]

    results = collection.aggregate(pipeline)
    vals = []
    for item in results:
        vals.append(f"{item['team_name']}, кол-во карточек: {item['total_yellow_red_cards']}")
    if vals:
        aggr_results.configure(values=vals)
        aggr_results.current(0)


def show_bombards():
    pipeline = [
        { '$unwind': '$goals' },
        {
            '$group': {
                '_id': '$goals.player_name',  
                'total_goals': { '$sum': 1 }   
            }
        },
        { 
         '$sort': { 
            'total_goals': -1 
            } 
        },
        { '$limit': 1 },
        {
        '$project': {
            'player_name': '$_id',
            'total_goals': 1,
            '_id': 0
            }
        }
    ]
    
    results = collection.aggregate(pipeline)
    vals = []
    for item in results:
        vals.append(f"{item['player_name']}, кол-во голов: {item['total_goals']}")
    if vals:
        aggr_results.configure(values=vals)
        aggr_results.current(0)

    
    
def aggr_wrapper():
    comand = agregate_comand_input.get()
    if comand == "Список бомбардиров":
        show_bombards()
    elif comand == "Команда c наибольшим количеством карточек":
        show_commands_with_cards()           
    
    
def show_search_results():
    key = search_key_input.get()
    value = search_value_input.get()
    comparer = comparer_converter[search_comparer_input.get()]
    
    value = {comparer: value}
    
    target = make_nested_dict(key, value)    
    projection = {"type": 1, "name": 1}
    vals = []
    for doc in collection.find(target, projection):
        vals.append(f"Тип: {doc.get('type', 'неизвестный')}. Название: {doc.get('name', 'не определено')}")
    results_combo.configure(values=vals)
    if vals:
        results_combo.current(0)


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
    for doc in collection.find():
        doc_str = json_util.dumps(doc, indent=2, ensure_ascii=False)
        delimeter = "\n" + "-" * docs_content_txt['width'] + "\n"
        docs_content_txt.insert(tk.END, doc_str + delimeter)

    
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

# Словари для отображения документов
documents_name = { }
searched_docs_name = { }

# Словарь для перевода знаков сравнения в ключи MongoDB
comparer_converter = { 
                      "<" : "$lt",
                      "<=" : "$lte",
                      "=" : "$eq",
                      ">=" : "$gte",
                      ">" : "$gt" 
                    }
 
 
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
search_key_input = tk.StringVar()
search_comparer_input = tk.StringVar()
search_value_input = tk.StringVar()

agregate_comand_input = tk.StringVar()

padx = 10

tk.Label(root, text="Текущий документ:").place(x=padx, y=10)

docs_combo = ttk.Combobox(root, width=40, textvariable=curr_doc, state="readonly")
update_docs_combo()
docs_combo.current(0)
docs_combo.place(x=padx, y=30)

tk.Label(root, text="Тип документа").place(x=padx, y=60)

options = ("Матч", "Команда")
ttk.Combobox(root, textvariable=document_name_input, values=options, state="readonly").place(x=padx, y=80)
tk.Button(root, text="Создать ещё документ", command=create_document).place(x=padx, y=110)

col_width = 340
tk.Label(root, text="Ключ или вложенные ключи (через точку):").place(x=padx + col_width, y=10)
tk.Entry(root, textvariable=key_input).place(x=padx + col_width, y=30)

tk.Label(root, text="Значение:").place(x=padx + col_width, y=60)
tk.Entry(root, textvariable=value_input).place(x=padx + col_width, y=80)

tk.Button(root, text="Добавить ключ-значение в текущий документ", command=insert_into_document_wrapper).place(x=padx + col_width, y=110)

tk.Button(root, text="Сохранить документ", command=save_document).place(x=padx + col_width, y=150)

padx = padx + col_width
col_width = 350
tk.Button(root, text="Показать документы", command=show_documents).place(x=padx+col_width, y=10)

docs_content_txt = tk.Text(root, width=50)
docs_content_txt.place(x=padx+col_width, y=50)

tk.Label(root, text="Ключ, по которому ведётся поиск:").place(x=1150, y=10)
tk.Entry(root, textvariable=search_key_input).place(x=1150, y=30)

vals = ['>', '>=', '=', '<=', '<']
search_combo = ttk.Combobox(root, values=vals, textvariable=search_comparer_input, width=3)
search_combo.current(0)
search_combo.place(x=1150, y=60)

tk.Label(root, text="Значение ключа, по которому ведётся поиск:").place(x=1150, y=90)
tk.Entry(root, textvariable=search_value_input).place(x=1150, y=110)
tk.Button(root, text="Показать результаты", command=show_search_results).place(x=1150, y=140)

results_combo = ttk.Combobox(root, state="readonly")
results_combo.place(x=1150, y=170)

tk.Label(root, text="Доступные команды для агрегации результатов:").place(x=10, y=450)
vals = ["Лучший бомбардир", "Команда c наибольшим количеством карточек"]
aggregate_combo = ttk.Combobox(root, values=vals, width=45, textvariable=agregate_comand_input, state="readonly")
aggregate_combo.place(x=10, y=470)

tk.Button(root, text="Применить", command=aggr_wrapper).place(x=10, y=500)

aggr_results = ttk.Combobox(root, width=55, state="readonly")
aggr_results.place(x=10, y=530)

root.mainloop()