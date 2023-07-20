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