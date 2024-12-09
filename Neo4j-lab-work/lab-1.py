from neo4j import GraphDatabase

# Подключаемся к серверу Neo4j
uri = "bolt://192.168.112.103:7687"
username = "neo4j"
password = "maiShoo7"

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_nodes_and_relationship(tx):
    # Создаем два узла и связь между ними
    query = (
        "CREATE (a:Person {name: 'Alice'}) "
        "CREATE (b:Person {name: 'Bob'}) "
        "CREATE (a)-[:FRIEND_WITH]->(b) "
        "RETURN a, b"
    )
    result = tx.run(query)
    for record in result:
        print(f"Созданы узлы: {record['a']['name']} и {record['b']['name']}")

def get_nodes_and_relationships(tx):
    # Получаем узлы и связи между ними
    query = (
        "MATCH (a:Person)-[r:FRIEND_WITH]->(b:Person) "
        "RETURN a, r, b"
    )
    result = tx.run(query)
    for record in result:
        print(f"Узел 1: {record['a']['name']}, Связь: FRIEND_WITH, Узел 2: {record['b']['name']}")

with driver.session() as session:
    # Создаем узлы и связь
    session.execute_write(create_nodes_and_relationship)
    # Получаем и выводим узлы и связь
    session.execute_read(get_nodes_and_relationships)
# Закрываем соединение
driver.close()