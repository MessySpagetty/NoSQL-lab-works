import redis

# Connect to Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set a key-value pair
client.set('my_key', 'Hello, Redis!')

# Retrieve the value
value = client.get('my_key')

print(value.decode('utf-8'))  # Output: Hello, Redis!
