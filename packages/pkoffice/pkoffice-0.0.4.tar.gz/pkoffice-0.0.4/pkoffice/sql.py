import sqlalchemy as sql
import pandas as pd


class SqlDB:
    """
    Class to manage sql database connection.
    """
    def __init__(self, server: str, database: str, driver: str):
        self.engine = sql.create_engine(f"mssql+pyodbc://{server}/"
                                        f"{database}?driver={driver}")

    def download_data(self, query: str) -> pd.DataFrame:
        """
        Method to download data from database according to provided query.
        :param query: SQL query in string format
        :return: pandas.Dataframe
        """
        with self.engine.begin() as conn:
            return pd.read_sql(sql=sql.text(query), con=conn)

    def execute_query(self, query: str) -> None:
        """
        Method to execute query
        :param query: SQL query in string format
        :return: None
        """
        with self.engine.begin() as conn:
            conn.execute(sql=sql.text(query))

    def upload_data(self, df: pd.DataFrame, table_name: str, chunksize: int,
                    if_exists: str = 'replace') -> None:
        """
        Method to upload pandas dataframe to database.
        :param df: pandas dataframe with data to upload
        :param table_name: name of table without []
        :param chunksize: size of single batch to upload
        :param if_exists: replace - drop/create, append - insert at the end
        :return: None
        """
        df.to_sql(table_name, con=self.engine, if_exists=if_exists,
                  index=False, chunksize=chunksize, method='multi', schema='dbo')

    def upload_log(self, table_name, log_value: list) -> None:
        """
        Method to upload log to database.
        :param table_name: log table name in SQL database
        :param log_value: list of values which needs to be uploaded
        :return: None
        """
        sql_values = [f"'{x}'" if type(x) == str else str(x) for x in log_value]
        sql_values = ','.join(sql_values)
        with self.engine.begin() as conn:
            conn.execute(
                f"""Insert into {table_name}
                Values ({sql_values})""")