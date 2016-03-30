from collections import namedtuple

import psycopg2

from comparison_dict import ComparisonDict
from config import db_name, user, host

SchemaElement = namedtuple('SchemaElement', 'name length datatype')


class Database(object):
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}'".format(
        db_name, user, host))

    def __enter__(self):
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()

    def fetch_all_as_dict(self, table_name: str):
        columns = self.get_table_columns(table_name)
        rows = []
        self.cur.execute('''SELECT * FROM {table_name};'''.format(table_name=table_name))

        for row in self.cur.fetchall():
            dict_row = ComparisonDict()
            for column, val in zip(columns, row):
                if column[1] == 'boolean':
                    dict_row[column[0]] = '1' if val else '0'
                else:
                    dict_row[column[0]] = val
            rows.append(dict_row)
        return rows


    def get_table_columns(self, table_name: str):
        query = '''
          SELECT column_name, data_type from INFORMATION_SCHEMA.COLUMNS
          WHERE table_name = '{table_name}';
        '''.format(table_name=table_name)
        self.cur.execute(query)

        return [(info[0], info[1]) for info in self.cur.fetchall()]

    def create_table_if_not_exists(self, table_name: str, schema: list):
        table_columns = ','.join(['{} {}'.format(item.name, item.datatype) for item in schema])
        query = '''
            CREATE TABLE IF NOT EXISTS {table_name}(
              {table_columns}
            );'''.format(table_name=table_name, table_columns=table_columns)
        self.cur.execute(query)

    def insert_rows(self, table_name: str, schema: list, data_rows: list):
        schema_names = [s.name for s in schema]

        def row_gen():
            for row in data_rows:
                yield '({vals})'.format(vals=', '.join((str(v) for v in row)))
        self.create_table_if_not_exists(table_name, schema)

        query = '''INSERT INTO {table_name} ({names}) VALUES {values};'''.format(
            table_name=table_name,
            names=', '.join(schema_names),
            values=', '.join((row for row in row_gen())))

        self.cur.execute(query)

    def remove_table(self, table_name: str):
        query = 'DROP TABLE {table_name};'.format(table_name=table_name)
        self.cur.execute(query)

    def table_exists(self, table_name: str) -> bool:
        query = '''SELECT relname FROM pg_class WHERE relname = '{}';'''.format(table_name)
        self.cur.execute(query)
        return True if self.cur.fetchone() else False

    def count_table_rows(self, table_name: str) -> int:
        query = 'SELECT count(*) AS count FROM {};'.format(table_name)
        self.cur.execute(query)
        try:
            return int(self.cur.fetchone()[0])
        except:
            return 0

