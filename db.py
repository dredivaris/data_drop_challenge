import psycopg2


class Database(object):
    conn = psycopg2.connect("dbname='clover' user='dredivaris' host='localhost'")

    def __enter__(self):
        self.cur = self.conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
