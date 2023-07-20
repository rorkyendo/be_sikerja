from mysql import connector
import pandas as pd
import os

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

class QueryBuilder():
    def __get_connection(self):
        return connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        
    def raw_query(self, query: str) -> pd.DataFrame:
        connection = self.__get_connection()
        data = pd.read_sql_query(query, connection)
        connection.close()
        
        return data
        
    def insert(self, table_name : str, data: pd.DataFrame):
        connection = self.__get_connection()
        cols = ",".join([str(i) for i in data.columns.tolist()])
        cursor = connection.cursor()

        # Insert DataFrame recrds one by one.
        for i,row in data.iterrows():
            sql = f"INSERT INTO {table_name} (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
            cursor.execute(sql, tuple(row))
            
        connection.commit()
        connection.close()