from pymongo.mongo_client import MongoClient
import tkinter.ttk as ttk
import tkinter as tk
import json
from bson import json_util


def get_general_cost_of_purchased_items(collection, result_area):
    raise NotImplementedError

def get_items_amount_in_each_category(collection, result_area):
    pipeline = [
        {
            '$group': {
                '_id': '$category',
                'amount': {'$sum': 1}
            } 
        },
        {
            '$project': {
                'category': '$_id',
                '_id': 0,
                'amount': 1
            }   
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    
    result_area.delete("1.0", tk.END)
    for item in cursor:
        result_area.insert(tk.END, f"Категория: {item['category']}. Количество: {item['amount']}.\n")
        
    
    

def exec_query_no_params():
    comand = command_no_params.get()
    if comand == "Получить количество товаров в каждой категории":
        get_items_amount_in_each_category(collection, result_area)
    elif comand == "Получить общую сумму проданных товаров":
        get_general_cost_of_purchased_items(collection, result_area)


def get_customers_of_items(item_name, collection, result_area):
    pipeline = [
        {
            "$match": {
                "product.name": item_name
            }
        },
        {
            "$unwind": "$customers"
        },
        {
            "$project": {
                "_id": 0,
                "customers.name": 1
            }
        }
    ]
    cursor = collection.aggregate(pipeline)
    
    result_area.delete("1.0", tk.END)
    for item in cursor:
        customer = item['customers']
        result_area.insert(tk.END, f"{customer['name']}\n")


def get_names_manufacturers_prices_for_item_with_color(color, collection, result_area):
    filter = {"product.color": color}
    projection = { "_id": 0, "product.name": 1, "product.manufacturer": 1, "product.price": 1}    

    cursor = collection.find(filter, projection)
    result_area.delete("1.0", tk.END)
    
    for item in cursor:
        item_pr = item['product'] 
        for ch in item_pr.keys():
            result_area.insert(tk.END, f"{ch}: {item_pr[ch]}\n")
        result_area.insert(tk.END, "-" * result_area["width"] + "\n")


def get_items_name_and_cost_for_customer(customer_name, collection, result_area):
    pipeline = [
        {
            "$unwind": "$customers"
        },
        {
            "$match": {
                "customers.name": customer_name
            }
        },
        {
            "$project": {
                "_id": 0,
                "product.name": 1,
                "product.price": 1
            }
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    result_area.delete("1.0", tk.END)
    
    pad = "  "
    result_area.insert(tk.END, f"{customer_name}\n")
    for item in cursor:
        for ch in item['product']:
            result_area.insert(tk.END, f"{pad}{ch}: {item['product'][ch]}\n")
        result_area.insert(tk.END, '\n')
    

def get_item_features_of_category(category, collection, result_area):
    filter = {"category": category}
    projection = { "_id": 0, "product.features": 1, "product.name": 1}
    
    cursor = collection.find(filter, projection)
    result_area.delete("1.0", tk.END)
    
    pad = "  "
    for item in cursor:
        result_area.insert(tk.END, f"{item['product']['name']}\n")
        features = item['product']['features']
        for feature in features.keys():
            result_area.insert(tk.END, f"{pad}{feature}: {features[feature]}\n")


def get_item_names_of_category(category, collection, result_area):
    filter = { "category": category }
    projection = {"_id": 0, "product.name": 1}
    
    cursor = collection.find(filter, projection)
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
        get_items_name_and_cost_for_customer(param, collection, result_area)
    elif comand == "Получить список названий, производителей и цен на товары, имеющие заданный цвет":
        get_names_manufacturers_prices_for_item_with_color(param, collection, result_area)
    elif comand == "Получить список имен покупателей заданного товара":
        get_customers_of_items(param, collection, result_area)
    

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
tk.Entry(root, textvariable=one_param_value).grid(row=2, column=1)

tk.Button(root, text="Выполнить запрос", command=exec_query_one_param).grid(row=4, column=1)

vals_no_params = ["Получить количество товаров в каждой категории", "Получить общую сумму проданных товаров"]
no_params_combo = ttk.Combobox(root, values=vals_no_params, textvariable=command_no_params, state="readonly", width=50)
no_params_combo.current(0)
no_params_combo.grid(row=0, column=3)

tk.Button(root, text="Выполнить запрос", command=exec_query_no_params).grid(row=2, column=3)

tk.Label(root, text="Результаты выполнения запроса:").grid(row=5, column=1)
result_area = tk.Text(root, width=50)
result_area.grid(row=6, column=1)

root.mainloop()