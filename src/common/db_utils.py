
import sqlite3
from dataclasses import asdict, is_dataclass
from typing import Type
import pandas as pd
import logging
import sys


class DatabaseExecutions:
    def __init__(self, db_name: str):
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()

    def create_table(self, table_name: str=None, schema: Type[object]=None, overwrite: bool = False,ddl_query=None):

        try:
            cursor = self._cursor
            if ddl_query:

                cursor.execute(ddl_query)
                self._conn.commit()
                return
            fields = []
            for field_name, field_definition in schema.__dict__.items():
                if not field_name.startswith('__'):
                    fields.append(f"{field_name} {field_definition}")
            fields_definition = ', '.join(fields)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_definition})"
            if overwrite:
                self.drop_table(table_name)
            cursor.execute(create_table_query)
            self._conn.commit()
        except Exception as e:
            pass

    def insert_data(self, table_name: str, schema_instance: object):
        try:
            cursor = self._cursor
            data_dict = asdict(schema_instance)
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['?'] * len(data_dict))
            values = tuple(data_dict.values())
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            print(values)
            cursor.execute(insert_query, values)
            self._conn.commit()
            return True
        except Exception as e:
            raise CustomException(e)
            return False

    def execute_query(self, query: str) -> pd.DataFrame:
        cursor = self._cursor
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return pd.DataFrame(rows, columns=column_names)

    def drop_table(self, table_name: str):
        cursor = self._cursor
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_query)
    #
    # def __del__(self):
    #     self._conn.close()

class CustomException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = error_message

    def __str__(self):
        return self.error_message

def error_message_detail(error: Exception, error_detail: sys):
    exc_tb = error_detail.exc_info
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script name [{file_name}] Line number [{exc_tb.tb_lineno}] error message [{str(error)}]"
    logging.error(error_message)
    return error_message
