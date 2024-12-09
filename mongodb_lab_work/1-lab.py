from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk


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
db[cl_name].insert_one({"type" : "Команда",
                        "team_name": "Грачи улицы",
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
                        ]}
                       )

db[cl_name].insert_one({"type": "Команда",
                        "team_name": "Динамо Львы",
                        "hometown": "Москва",
                        "trainer": "Виктор Петрович Сидоров",
                        "start_position": [
                            {'player_name': 'Александр Сергеевич Пушкин', 'position': 'Вратарь'},
                            {'player_name': 'Игорь Викторович Мясников', 'position': 'Защитник'},
                            {'player_name': 'Станислав Николаевич Краснов', 'position': 'Защитник'},
                            {'player_name': 'Денис Андреевич Кузьмичев', 'position': 'Защитник'},
                            {'player_name': 'Валентин Олегович Ершов', 'position': 'Защитник'},
                            {'player_name': 'Алла Николаевна Варенникова', 'position': 'Полузащитник'},
                            {'player_name': 'Кирилл Павлович Лебедев', 'position': 'Полузащитник'},
                            {'player_name': 'Наталья Владимировна Ильина', 'position': 'Полузащитник'},
                            {'player_name': 'Николай Сергеевич Сапрыкин', 'position': 'Нападающий'},
                            {'player_name': 'Федор Дмитриевич Романов', 'position': 'Нападающий'},
                            {'player_name': 'Станислав Александрович Бодров', 'position': 'Нападающий'}
                        ],
                        "substitute_players": [
                            {'player_name': 'Ирина Константиновна Чернова', 'position': 'Запасной'},
                            {'player_name': 'Вадим Алексеевич Прохоров', 'position': 'Запасной'},
                            {'player_name': 'Анна Викторовна Баранова', 'position': 'Запасной'}
                        ]}
                        )

db[cl_name].insert_one({"type": "Команда",
                        "team_name": "Звездные Молнии",
                        "hometown": "Новосибирск",
                        "trainer": "Светлана Викторовна Нестерова",
                        "start_position": [
                            {'player_name': 'Павел Иванович Соловьев', 'position': 'Вратарь'},
                            {'player_name': 'Максим Анатольевич Марков', 'position': 'Защитник'},
                            {'player_name': 'Кирилл Олегович Гордеев', 'position': 'Защитник'},
                            {'player_name': 'Евгений Борисович Павлов', 'position': 'Защитник'},
                            {'player_name': 'Михаил Валерьевич Дьяченко', 'position': 'Защитник'},
                            {'player_name': 'Юлия Викторовна Селиверстова', 'position': 'Полузащитник'},
                            {'player_name': 'Роман Петрович Новиков', 'position': 'Полузащитник'},
                            {'player_name': 'Илья Сергеевич Соловьев', 'position': 'Полузащитник'},
                            {'player_name': 'Артем Владимирович Кантемиров', 'position': 'Нападающий'},
                            {'player_name': 'Денис Борисович Григорьев', 'position': 'Нападающий'},
                            {'player_name': 'Григорий Степанович Ласточкин', 'position': 'Нападающий'}
                        ],
                        "substitute_players": [
                            {'player_name': 'Кристина Анатольевна Скуратова', 'position': 'Запасной'},
                            {'player_name': 'Светослав Дмитриевич Лебедев', 'position': 'Запасной'},
                            {'player_name': 'Елена Александровна Орлова', 'position': 'Запасной'}
                        ]}
                        )

db[cl_name].insert_one({"type" : "Игра",
                        "date_of_match": "11.10.2024",
                        "match_score": "1-0",
                        "yellow-red-cards": [       
                            {"color": "yellow", 
                             "player_name" : "Пётр Васильевич Петрович", 
                             "minute" : 7, 
                             "reason": "Несанцкционированный выход на поле"
                            } 
                        ],
                        "goals": [
                            {"player_name": "Иван Сергеев Сергеевич",
                            "minute": 10,
                            "pass": "Сергей Николаев Сергеевич", 
                            "position": "Защитник"
                            }
                        ],                       
                        "penalties": [
                            {"player_name": "Иван Сергеев Сергеевич",
                            "minute": 15,
                            "pass": "Сергей Николаев Сергеевич",
                            "position": "Пенальти"
                            }
                        ],
                        "gate_strikes": [
                            {"player_name": "Иван Сергеев Сергеевич",
                            "minute": 10,
                            "pass": "Антон Тимофеев Антонович",
                            "position": "Нападающий"
                            }
                        ]
                        })

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