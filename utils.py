import csv
import math
import os
import logging
import sys

from models import FilmWork, Person, Genre, PersonFilmWork, GenreFilmWork

class SQLiteLoader():
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def load_tables_names(self):
        try:
            tables_names = self.cursor.\
                execute("SELECT name FROM sqlite_master WHERE type='table';")
        except Exception as e:
            logging.exception()
            sys.exit()

        arr_tables_names = []
        check_tables_names = [arr_tables_names.append(i[0]) for i in tables_names]

        return arr_tables_names

    def load_table_columns_info(self, table_name):
        try:
            table_info = self.cursor.execute(f"PRAGMA table_info({table_name});")
        except Exception as e:
            logging.exception()

        clear_data_table_info = []
        for i in table_info:
            clear_data_table_info.append(i[1])
        return clear_data_table_info

    def forming_attrs_and_attrs_for_unconflict(self, table_name: str, table_info):
        attrs = []
        attrs_with_id = []
        for i in table_info:
            attrs.append(i)
            """формируем список для избежания конфликтных ситуаций при запросе"""
            if table_name == 'person_film_work' or table_name == 'genre_film_work':
                var_id = '_id'
            else:
                var_id = 'id'
            if i.find(var_id) > -1:
                attrs_with_id.append(i)

        attrs = ", ".join(attrs)
        attrs_with_id = ", ".join(attrs_with_id)
        return attrs, attrs_with_id

    def load_data(self, table_name: str, attrs, quantity, data_file_paths):
        try:
            catch_data = self.cursor.execute(f"select * from {table_name}")
        except Exception as e:
            logging.exception()
        count_rows = math.ceil(int(len(list(self.cursor)))/quantity)

        try:
            query = self.cursor.execute(f"select * from {table_name}")
        except Exception as e:
            logging.exception()

        file_path = f'{table_name}.csv'
        while count_rows:
            data_array = self.cursor.fetchmany(quantity)
            file_path = self.copy_to_csv(file_path, data_array, table_name)
            count_rows -= 1

        data_file_paths.append(file_path)

    def copy_to_csv(self,file_path, data_array, table_name):

        with open(file_path, 'a+') as f:
            writer = csv.writer(f)
            for row in data_array:
                values = []
                counter = 0
                for value in row:
                    if value is None:
                        if counter == 2 or counter == 3 or counter == 4 or counter == 5:
                            value = ""
                        if counter == 6:
                            value = float()
                    counter += 1

                    values.append(value)

                if table_name == 'film_work':
                    check_value = FilmWork(
                        id=values[0],
                        title=values[1],
                        description=values[2],
                        creation_date=values[3],
                        certificate=values[4],
                        file_path=values[5],
                        rating=values[6],
                        type=values[7],
                        created_at=values[8],
                        updated_at=values[9]
                    )
                if table_name == 'person':
                    check_value = Person(
                        id=values[0],
                        full_name=values[1],
                        birth_date=values[2],
                        created_at=values[3],
                        updated_at=values[4]
                    )
                if table_name == 'genre':
                    check_value = Genre(
                        id=values[0],
                        name=values[1],
                        description=values[2],
                        created_at=values[3],
                        updated_at=values[4]
                    )
                if table_name == 'person_film_work':
                    check_value = PersonFilmWork(
                        id=values[0],
                        film_work_id=values[1],
                        person_id=values[2],
                        role=values[3],
                        created_at=values[4]
                    )
                if table_name == 'genre_film_work':
                    check_value = GenreFilmWork(
                        id=values[0],
                        film_work_id=values[1],
                        genre_id=values[2],
                        created_at=values[3],
                    )
                writer.writerow(values)
        return file_path


    def create_cols_slots(self, table_name):
        counter = 0
        with open(self.link_to_path(table_name)) as file:
            data_reader = csv.reader(file)
            for index, line in enumerate(data_reader):
                if index == 0:
                    headings = line

        for _ in headings:
            counter += 1
        cols_slots = f"({'%s, ' * (counter - 1)}{'%s'})"
        return cols_slots

    def link_to_path(self, table_name):
        return f'{table_name}.csv'


class PostgresSaver:
    def __init__(self, pg_cursor):
        self.pg_cursor = pg_cursor

    def save_all_data(self, table_name, cols_slots, attrs, attrs_with_id, sqlite_loader):

        with open(sqlite_loader.link_to_path(table_name)) as file:
            data_reader = csv.reader(file)
            data = []
            for row in data_reader:
                values = []
                for value in row:
                    if value == "":
                        value = None

                    values.append(value)
                data.append(values)

        try:
            args = ','.join(self.pg_cursor.mogrify(cols_slots, item).decode() for item in data)
            self.pg_cursor.execute(f"""
            INSERT INTO content.{table_name} ({attrs})
            VALUES {args}
            ON CONFLICT ({attrs_with_id}) DO NOTHING
            """)

        except Exception as e:
            logging.exception()
        else:
            # удаляем отработанные файлы
            os.remove(sqlite_loader.link_to_path(table_name))
