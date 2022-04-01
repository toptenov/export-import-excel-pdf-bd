from modules.db_import import *
from modules.db_export import  *
import sqlite3


def main():
    if not os.path.exists('server.sqlite3'):
        create_sql_file()
        initial_db_creation()

    create_result_directories()

    db = sqlite3.connect('server.sqlite3')
    sql = db.cursor()

    while True:
        user_input = input('Do you want to import (i) or export (e) data: ')
        if user_input.lower() in 'i':
            user_input = input('Do you want to import data from excel (e) or pdf (p): ')
            if user_input.lower() == 'e':
                import_data_from_excel(db, sql)
            elif user_input.lower() == 'p':
                import_data_from_pdf(db, sql)
            else:
                break
        elif user_input.lower() in 'e':
            user_input = input('Do you want to export data to excel (e) or pdf (p): ')
            if user_input.lower() == 'e':
                export_data_to_excel(db)
            elif user_input.lower() == 'p':
                export_data_to_pdf(db)
            else:
                break
        else:
            break


if __name__ == '__main__':
    main()
