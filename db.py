from collections import namedtuple

import psycopg2

SchemaElement = namedtuple('SchemaElement', 'name datatype')


class Database(object):
    conn = psycopg2.connect("dbname='clover' user='dredivaris' host='localhost'")

    def __enter__(self):
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()

    def fetch_all(self, table_name: str, schema: SchemaElement):
        self.cur.execute('''SELECT * FROM {table_name};'''.format(table_name=table_name))
        print(self.cur.fetchall())

    def create_table_if_not_exists(self, table_name: str, schema: list):
        table_columns = ','.join(['{} {}'.format(item.name, item.datatype) for item in schema])
        query = '''
            CREATE TABLE IF NOT EXISTS {table_name}(
              {table_columns}
            );'''.format(table_name=table_name, table_columns=table_columns)
        self.cur.execute(query)





