import json
import sqlite3

import openpyxl
from pdfminer.high_level import extract_text

with open("./modules/cities_and_regions.json", "r") as read_file:
    data = json.load(read_file)

CITIES_AND_REGIONS = {}
for i in range(len(data)):
    for key, value in data[i].items():
        CITIES_AND_REGIONS[key] = value


def add_a_comma_if_necessary(sql_insert):
    if sql_insert[-1:-8:-1][::-1] not in 'VALUES ':
        sql_insert += ', '
    return sql_insert


def execute_and_commit_in_db(db, sql, sql_insert):
    sql.execute(sql_insert)
    db.commit()
    print("\n" + sql_insert + "\n")


def import_users_to_db(db, sql, users_data):
    users_sql_insert = f'INSERT INTO users ' \
                       f'(region_id, city_id, first_name, second_name, patronymic, phone, email) VALUES '

    for user in users_data:
        users_sql_insert = add_a_comma_if_necessary(users_sql_insert)
        users_sql_insert += f'({user["region_id"]}' \
                            f', {user["city_id"]}' \
                            f', "{user["first_name"]}"' \
                            f', "{user["second_name"]}"' \
                            f', "{user["patronymic"]}"' \
                            f', "{user["phone"]}"' \
                            f', "{user["email"]}")'

    execute_and_commit_in_db(db, sql, users_sql_insert)


def import_regions_to_db(db, sql, regions_data):
    regions_sql_insert = f'INSERT INTO regions (region_name) VALUES '

    for region in regions_data:
        regions_sql_insert = add_a_comma_if_necessary(regions_sql_insert)
        regions_sql_insert += f'("{region["region_name"]}")'

    execute_and_commit_in_db(db, sql, regions_sql_insert)


def import_cities_to_db(db, sql, cities_data):
    cities_sql_insert = f'INSERT INTO cities (region_id, city_name) VALUES '

    for city in cities_data:
        cities_sql_insert = add_a_comma_if_necessary(cities_sql_insert)
        cities_sql_insert += f'({city["region_id"]}' \
                             f', "{city["city_name"]}")'

    execute_and_commit_in_db(db, sql, cities_sql_insert)


def initial_data_filling(db, sql):
    # Fill the regions-table with initial data
    regions_data = [
        {'region_name': 'Краснодарский край'},
        {'region_name': 'Ростовская область'},
        {'region_name': 'Ставропольский край'}
    ]
    import_regions_to_db(db, sql, regions_data)
    print("The table \"regions\" has been successfully updated with initial data")

    # Fill the cities-table with initial data
    cities_data = [
        {'region_id': 1, 'city_name': 'Краснодар'},
        {'region_id': 1, 'city_name': 'Кропоткин'},
        {'region_id': 1, 'city_name': 'Славянск'},
        {'region_id': 2, 'city_name': 'Ростов'},
        {'region_id': 2, 'city_name': 'Шахты'},
        {'region_id': 2, 'city_name': 'Батайск'},
        {'region_id': 3, 'city_name': 'Ставрополь'},
        {'region_id': 3, 'city_name': 'Пятигорск'},
        {'region_id': 3, 'city_name': 'Кисловодск'}
    ]
    import_cities_to_db(db, sql, cities_data)
    print("The table \"cities\" has been successfully updated with initial data")

    # Fill the users-table with initial data
    users_data = [
        {'region_id': 1, 'city_id': 1, 'first_name': 'Игорь', 'second_name': 'Летов',
         'patronymic': 'Федорович', 'phone': '+7(965)1112241', 'email': 'email1@email.com'},
        {'region_id': 3, 'city_id': 9, 'first_name': 'Иван', 'second_name': 'Иванов',
         'patronymic': 'Иванович', 'phone': '+7(965)1112242', 'email': 'email2@email.com'},
        {'region_id': 2, 'city_id': 5, 'first_name': 'Григорий', 'second_name': 'Шишкин',
         'patronymic': 'Казимирович', 'phone': '+7(965)1112243', 'email': 'email3@email.com'}
    ]
    import_users_to_db(db, sql, users_data)
    print("The table \"users\" has been successfully updated with initial data")


def create_sql_file():
    with open('server.sqlite3', "w"):
        print("SQLite3 file has been successfully created")


def initial_db_creation():
    db = sqlite3.connect('server.sqlite3')
    sql = db.cursor()

    sql.execute(
        '''
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_name VARCHAR(100) NOT NULL UNIQUE
        )
        '''
    )
    print("A table \"regions\" has been successfully created")

    sql.execute(
        '''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INT NOT NULL,
            city_name VARCHAR(50) NOT NULL UNIQUE,
            FOREIGN KEY (region_id) REFERENCES regions(id)
        )
        '''
    )
    print("A table \"cities\" has been successfully created")

    sql.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            second_name VARCHAR(50) NOT NULL,
            patronymic VARCHAR(50) NOT NULL,
            region_id INT NOT NULL NOT NULL,
            city_id INT NOT NULL NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(50) NOT NULL UNIQUE,
            FOREIGN KEY (region_id) REFERENCES regions(id),
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
        '''
    )
    print("A table \"users\" has been successfully created")

    db.commit()

    initial_data_filling(db, sql)


def import_data_from_excel(db, sql):
    # Collect data from excel:
    book = openpyxl.load_workbook('./sources/Source.xlsx')
    sheet_regions = book["regions"]
    sheet_cities = book["cities"]
    sheet_users = book["users"]

    # Input regions from excel to db:
    regions_data = []
    row = 2
    empty_cell = False
    while not empty_cell:
        if sheet_regions[row][0].value is None:
            empty_cell = True

        if not empty_cell:
            regions_data.append(
                {
                    'region_name': sheet_regions[row][0].value
                }
            )
            row += 1

    import_regions_to_db(db, sql, regions_data)

    # Input cities from excel to db:
    cities_data = []
    row = 2
    empty_cell = False
    while not empty_cell:
        for column in range(2):
            if sheet_cities[row][column].value is None:
                empty_cell = True

        if not empty_cell:
            cities_data.append(
                {
                    'region_id': sheet_cities[row][0].value,
                    'city_name': sheet_cities[row][1].value
                }
            )
            row += 1

    import_cities_to_db(db, sql, cities_data)

    # Input users from excel to db:
    users_data = []
    row = 2
    empty_cell = False
    while not empty_cell:
        for column in range(7):
            if sheet_users[row][column].value is None:
                empty_cell = True

        if not empty_cell:
            users_data.append(
                {
                    'region_id': sheet_users[row][0].value,
                    'city_id': sheet_users[row][1].value,
                    'first_name': sheet_users[row][2].value,
                    'second_name': sheet_users[row][3].value,
                    'patronymic': sheet_users[row][4].value,
                    'phone': sheet_users[row][5].value,
                    'email': sheet_users[row][6].value
                }
            )
            row += 1

    import_users_to_db(db, sql, users_data)


def import_data_from_pdf(db, sql):
    text_from_pdf = extract_text('./sources/Source.pdf')
    list_from_pdf = text_from_pdf.split()
    list_from_pdf[22] = list_from_pdf[22].strip(',')
    users_data = [
        {
            'first_name': list_from_pdf[1],
            'second_name': list_from_pdf[0],
            'patronymic': list_from_pdf[2],
            'region_name': CITIES_AND_REGIONS[list_from_pdf[22]],
            'city_name': list_from_pdf[22],
            'phone': list_from_pdf[10] + list_from_pdf[11] + list_from_pdf[12],
            'email': list_from_pdf[17]
         }
    ]

    # Import a region from pdf into db:
    sql.execute(f'SELECT * FROM regions WHERE region_name = "{users_data[0]["region_name"]}"')
    fetchone = sql.fetchone()
    if fetchone is None:
        import_regions_to_db(db, sql, [{'region_name': users_data[0]['region_name']}])
        sql.execute(f'SELECT id FROM regions WHERE region_name = "{users_data[0]["region_name"]}"')
        region_id_from_db = sql.fetchone()[0]
    else:
        region_id_from_db, region_name_from_db = fetchone

    # Import a city from pdf into db:
    sql.execute(f'SELECT id, city_name FROM cities WHERE city_name = "{users_data[0]["city_name"]}"')
    fetchone = sql.fetchone()
    if fetchone is None:
        cities_data = [
            {
                'region_id': region_id_from_db,
                'city_name': users_data[0]['city_name']
            }
        ]
        import_cities_to_db(db, sql, cities_data)
        sql.execute(f'SELECT id FROM cities WHERE city_name = "{users_data[0]["city_name"]}"')
        city_id_from_db = sql.fetchone()[0]
    else:
        city_id_from_db, city_name_from_db = fetchone

    # Import a user from pdf into db:sql.fetchone()
    users_data[0]['region_id'], users_data[0]['city_id'] = region_id_from_db, city_id_from_db
    import_users_to_db(db, sql, users_data)
