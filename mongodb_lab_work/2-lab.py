from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk
import json
from bson import json_util


def get_item_features_of_category(category, collection, result_area):
    raise NotImplementedError


def get_item_names_of_category(category, collection, result_area):
    query = { "category": category }
    projection = {"_id": 0, "product.name": 1}
    
    cursor = collection.find(query, projection)
    result_area.delete("1.0", tk.END)
    for item in cursor:
        result_area.insert(tk.END, f"{item['product']['name']}\n")


def exec_query_one_param():
    comand = comand_one_param.get()
    param = one_param_value.get()
    if comand == "Получить список названий товаров, относящихся к заданной категории":
        get_item_names_of_category(param, collection, result_area)
    elif comand == "Получить список характеристик товаров заданной категории":
        get_item_features_of_category(param, collection, result_area)
    elif comand == "Получить список названий и стоимости товаров, купленных заданным покупателем":
        raise NotImplementedError
    elif comand == "Получить список названий, производителей и цен на товары, имеющие заданный цвет":
        raise NotImplementedError
    elif comand == "Получить список имен покупателей заданного товара":
        raise NotImplementedError
    

def exec_query_two_params():
    cmp_name = company_name.get()
    pr_name = item_name.get()
    
    pipeline = [
        {
           "$match": {
                "product.name": pr_name,
                "product.manufacturer": cmp_name   
            }
        },
        {
            "$unwind": "$customers"
        },
        { 
            "$project": 
                { "_id": 0, "name": "$customers.name" } 
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    result_area.delete("1.0", tk.END)
    for item in cursor:
        result_area.insert(tk.END, f"{item['name']}\n")


# Подключение к БД
port="22304"
uri=f'mongodb://localhost:{port}'
db_name = '1-lab-db'

client = MongoClient(uri)
db = client[db_name]

# Инициализация коллекций
for coll in db.list_collection_names():
    db[coll].drop()

cl_name = "products_and_customers"
db.create_collection(cl_name, check_exists=False)

collection = db[cl_name]

with open('products_and_customers.json', 'r', encoding='utf-8') as json_file:
    db[cl_name].insert_many(json.load(json_file))


# Создание основного окна и установка его заголовка
root = tk.Tk()
root.title("Информация о товарах")

SCR_WIDTH = root.winfo_screenwidth() 
SCR_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCR_WIDTH}x{SCR_HEIGHT}")

comand_two_params = tk.StringVar()
item_name = tk.StringVar()
company_name = tk.StringVar()

comand_one_param = tk.StringVar()
one_param_name = tk.StringVar(value="Наименование категории:")
one_param_value = tk.StringVar()

command_no_params = tk.StringVar()


vals_two_params = ["Получить список имен покупателей заданного товара, с доставкой фирмы с заданным названием"]
two_param_combo = ttk.Combobox(root, values=vals_two_params, textvariable=comand_two_params, state="readonly", width=92)
two_param_combo.current(0)
two_param_combo.grid(row=0, column=0)

tk.Label(root, text="Наименование товара:").grid(row=1, column=0)
tk.Entry(root, textvariable=item_name).grid(row=2, column=0)
tk.Label(root, text="Наименование фирмы:").grid(row=3, column=0)
tk.Entry(root, textvariable=company_name).grid(row=4, column=0)

tk.Button(root, text="Выполнить запрос", command=exec_query_two_params).grid(row=5, column=0)

vals_one_param=[
        "Получить список названий товаров, относящихся к заданной категории", 
        "Получить список характеристик товаров заданной категории",
        "Получить список названий и стоимости товаров, купленных заданным покупателем",
        "Получить список названий, производителей и цен на товары, имеющие заданный цвет",
        "Получить список имен покупателей заданного товара"
        ]

one_param_combo = ttk.Combobox(root, values=vals_one_param, textvariable=comand_one_param, state="readonly", width=70)
one_param_combo.current(0)
one_param_combo.grid(row=0, column=1)

tk.Label(root, textvariable=one_param_name).grid(row=1, column=1)
tk.Entry(root, textvariable=one_param_value).grid(row=3, column=1)
tk.Button(root, text="Выполнить", command=exec_query_one_param).grid(row=4, column=1)

vals_no_params = ["Получить количество товаров в каждой категории", "Получить общую сумму проданных товаров"]
no_params_combo = ttk.Combobox(root, values=vals_no_params, textvariable=command_no_params, state="readonly", width=50)
no_params_combo.current(0)
no_params_combo.grid(row=0, column=3)

tk.Label(root, text="Результаты выполнения запроса:").grid(row=5, column=1)
result_area = tk.Text(root, width=50)
result_area.grid(row=6, column=1)

root.mainloop()