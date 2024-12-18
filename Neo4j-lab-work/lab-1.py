from neo4j import GraphDatabase

# Подключаемся к серверу Neo4j
uri = "bolt://192.168.112.103:7687"
username = "neo4j"
password = "maiShoo7"

driver = GraphDatabase.driver(uri, auth=(username, password))

from neo4j import GraphDatabase

def drop_all_data(driver):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def create_routes(driver):
    with driver.session() as session:
        session.run(
            "CREATE (:Route {id: 'Route101', name: 'Маршрут 101'}), "
                "(:Route {id: 'Route102', name: 'Маршрут 102'}), "
                "(:Route {id: 'Route103', name: 'Маршрут 103'}), "
                "(:Route {id: 'Route104', name: 'Маршрут 104'}), "
                "(:Route {id: 'Route105', name: 'Маршрут 105'})"
        )


def create_stops(driver):
    stops = [f'Oстановка {i}' for i in range(1, 21)]
    with driver.session() as session:
        for i, stop in enumerate(stops, start=1):
            session.run(f"CREATE (:Stop {{id: 'Stop{i}', name: '{stop}'}})")


def create_organizations(driver):
    organizations = [f'Организация {i}' for i in range(1, 21)]
    with driver.session() as session:
        for idx, org in enumerate(organizations, start=1):
            session.run(f"CREATE (:Organization {{id: 'Org{idx}', name: '{org}'}})")


def create_relationships(driver):
    route_map = {
        'Route101': ['Stop1', 'Stop2', 'Stop3', 'Stop4', 'Stop5'],
        'Route102': ['Stop6', 'Stop7', 'Stop8', 'Stop9', 'Stop10'],
        'Route103': ['Stop11', 'Stop12', 'Stop13'],
        'Route104': ['Stop14', 'Stop15', 'Stop16'],
        'Route105': ['Stop17', 'Stop18', 'Stop19', 'Stop20']
    }
    
    with driver.session() as session:
        for route_id, stops in route_map.items():
            for i, stop_id in enumerate(stops, start=1):
                session.run(
                    "MATCH (r:Route {id: $routeId}), (s:Stop {id: $stopId}) "
                    "CREATE (r)-[:STOPS_AT {order: $idx}]->(s)",
                    routeId=route_id,
                    stopId=stop_id, 
                    idx=i
                )

        for i in range(1, 21):
            stop_id = f'Stop{i}'
            org_id = f'Org{i}'
            session.run(
                "MATCH (s:Stop {id: $stopId}), (o:Organization {id: $orgId}) "
                "CREATE (s)-[:NEAR]->(o)", 
                stopId=stop_id,
                orgId=org_id
            )

def get_stops_for_route(driver, route_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (route:Route {id: $routeId})-[consist:STOPS_AT]->(stop:Stop) "
            "RETURN stop.name AS name, " 
            "consist.order AS order "
            "ORDER BY consist.order ASC",
            routeId=route_id
        )
        stops = [{"name": record["name"], "order": record["order"]} for record in result]
    return stops


def get_nearby_organizations(driver, stop_id):
    with driver.session() as session:
        result = session.run(
            f"MATCH (s:Stop {{id: '{stop_id}'}})-[:NEAR]->(o:Organization) "
            "RETURN o"
        )
        return [record["o"]["name"] for record in result]


def print_stops_for_routs(route, stops):
    print(f"Остановки для {route}:")
    for st in stops:
        print(f"{st['order']}: {st['name']}")
    print("")

# Инициализация БД
drop_all_data(driver)
create_routes(driver)
create_stops(driver)
create_organizations(driver)
create_relationships(driver)

print_stops_for_routs("Route101", get_stops_for_route(driver, "Route101"))

# Закрываем соединение
driver.close()