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

    def insert(self, table_name: str, data: pd.DataFrame):
        data.to_sql(table_name, self.engine, if_exists='append', index=False)
