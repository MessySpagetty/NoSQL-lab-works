from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk


def get_team_documents(collection):
    query = {'team': {'$exists': True}}
    teams = [doc['team'] for doc in collection.find(query)]
    return teams


def get_game_documents(collection):
    query = {'date': {'$exists': True}}
    dates = [doc['date'] for doc in collection.find(query)]
    return dates


def get_team_and_game_documents():
    collection = db[cl_name]
    # print(get_game_documents(collection), get_team_documents(collection))
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
db[cl_name].insert_one({"type" : "Команда",
                        "hometown": "Санкт_Петербург",
                        "trainer": "Суровый Антон Васильевич",
                        "start_position": [
                            {'player_name': 'Иван Сергеев Сергеевич', 'position': 'Вратарь'},
                            {'player_name': 'Петр Васильев Петрович', 'position': 'Защитник'},
                            {'player_name': 'Сергей Николаев Сергеевич', 'position': 'Защитник'},
                            {'player_name': 'Александр Владимиров Александрович', 'position': 'Защитник'},
                            {'player_name': 'Дмитрий Кириллов Дмитриевич', 'position': 'Защитник'},
                            {'player_name': 'Владимир Ильич Смирнов', 'position': 'Полузащитник'},
                            {'player_name': 'Евгений Александрович Кузнецов', 'position': 'Полузащитник'},
                            {'player_name': 'Николай Федоров Николаевич', 'position': 'Полузащитник'},
                            {'player_name': 'Антон Тимофеев Антонович', 'position': 'Нападающий'},
                            {'player_name': 'Максим Викторов Максимович', 'position': 'Нападающий'},
                            {'player_name': 'Никита Ломанов Александрович', 'position': 'Нападающий'}
                        ],
                        "substitute_players": [
                            {'player_name': 'Алексей Дмитриевич Сидоров', 'position': 'Запасной'},
                            {'player_name': 'Максим Иванович Ковалев', 'position': 'Запасной'},
                            {'player_name': 'Дмитрий Андреевич Смирнов', 'position': 'Запасной'}
                        ]})

db[cl_name].insert_one({"type" : "Игра"})

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

docs_combo = ttk.Combobox(root, values=get_team_and_game_documents(), textvariable=curr_doc, state="readonly")
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