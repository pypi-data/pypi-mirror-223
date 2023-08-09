from airflow.providers.postgres.operators.postgres import PostgresOperator


class UpdateLastUpdateDateOperator(PostgresOperator):

    def __init__(self, last_update_date: str, table_name: str, **kwargs):
        self.last_update_date = last_update_date
        self.table_name = table_name
        self.sql = f"UPDATE checkpoints SET last_update_date = '{self.last_update_date}' WHERE table = '{self.table_name}';"
        super().__init__(**kwargs)


class GetLastUpdateDateOperator(PostgresOperator):

    def __init__(self, table_name: str, **kwargs):
        
        self.table_name = table_name
        self.sql = f"SELECT last_update_date FROM checkpoints WHERE table = '{self.table_name}"
        super().__init__(**kwargs)
