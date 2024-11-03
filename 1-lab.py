import redis

with open('host', 'r') as file:
    HOST = file.read()  # Reads the entire file

with open('passwd', 'r') as file:
    PASSWORD = file.read()

client = redis.StrictRedis(host=HOST, password=PASSWORD)

# Префикс для уникальности ключей, чтобы совместно работать в БД
my_prefix = "poskitt_22304_"

# Set a key-value pair
client.set(my_prefix + 'my_key', 'Hello, Redis!')

# Retrieve the value
value = client.get(my_prefix + 'my_key')

print(value.decode('utf-8'))  # Output: Hello, Redis!
