import psycopg2
import config
from db.models import BaseModel


class SQLHandler:

    def connect(self):
        return psycopg2.connect(**config.DB_DATA)

    def version(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT version()')
                version = cur.fetchone()
                print(*version)

    def insert(self, model: BaseModel, table_name: str):
        value = model.asdict()
        keys = value.keys()
        columns = ', '.join(keys)
        mask = ', '.join(f'%({string})s' for string in keys)
        with self.connect() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({mask});', value)
                    conn.commit()
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    raise

    def select_max(self, column_name: str, table_name: str):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT MAX({column_name}) FROM {table_name};")
                return cur.fetchone()

    def request(self, req: str) :
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(req)
                return cur.fetchall()
