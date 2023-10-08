import pandas as pd
from sqlalchemy import create_engine
import os

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

class QueryBuilder():
    def __init__(self):
        # Create an SQLAlchemy engine at the initialization of the class
        self.engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    def raw_query(self, query: str) -> pd.DataFrame:
        # Use the engine directly with read_sql_query
        data = pd.read_sql_query(query, self.engine)
        return data
    
    def select_where_dict(self, table_name, condition: dict) -> pd.DataFrame:
        sql = f"SELECT * FROM {table_name} WHERE "
        where = ''
        for column_name, value in condition.items():
            if type(value) == str:
                where += f"{column_name} = '{value}' AND "
            elif value is None:
                where += f"{column_name} IS NULL AND "
            else:
                where += f"{column_name} = {value} AND "
        where = where[:-5]
        sql = sql + where
        
        return self.raw_query(sql)
    
    def insert_if_not_exist(self, table_name: str, data: pd.DataFrame):
        data = data.to_dict(orient='records')
        need_to_insert = []

        for d in data:
            # Check for duplicates based on 'nama_loker' and 'perusahaan' columns
            duplicate_condition = {
                'nama_loker': d['nama_loker'],
                'perusahaan': d['perusahaan']
            }

            # Fetch existing data from the database based on the duplicate_condition
            data_in_db = self.select_where_dict(table_name, duplicate_condition)

            # If no matching records found, add the data to need_to_insert list
            if data_in_db.empty:
                need_to_insert.append(d)

        if len(need_to_insert) > 0:
            self.insert(table_name, pd.DataFrame(need_to_insert))

    def insert(self, table_name: str, data: pd.DataFrame):
        data.to_sql(table_name, self.engine, if_exists='append', index=False)
