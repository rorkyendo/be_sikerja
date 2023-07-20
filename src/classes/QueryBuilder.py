from mysql import connector
import pandas as pd

class QueryBuilder():
    def __get_connection(self):
        return connector.connect(
            host="localhost",
            user="sikerja",
            password="sikerja",
            database="sikerja"
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