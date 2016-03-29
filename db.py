from collections import namedtuple

import psycopg2

SchemaElement = namedtuple('SchemaElement', 'name length datatype')


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

    def insert_rows(self, table_name, schema, data_rows):
        schema_names = [s.name for s in schema]

        # TODO: do we need a generator here? may be confusing for future devs
        def row_gen():
            for row in data_rows:
                yield '({vals})'.format(vals=', '.join((v for v in row)))
        gen = row_gen()

        query = '''
            INSERT INTO {table_name} ({names}) VALUES {values};
                (1, 'Cheese', 9.99),
                (2, 'Bread', 1.99),
                (3, 'Milk', 2.99);
        '''.format(
            table_name=table_name,
            names=', '.join(schema_names),
            values=', '.join((row for row in row_gen)))

        print(query)