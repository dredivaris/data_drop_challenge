from db import Database, SchemaElement


class TestDatabase():
    schema = [
        SchemaElement(name='name', length=10, datatype='TEXT'),
        SchemaElement(name='valid', length=1, datatype='BOOLEAN'),
        SchemaElement(name='count', length=3, datatype='INTEGER')]

    def test_create_table_if_not_exists_and_remove_table(self):
        with Database() as db:
            db.create_table_if_not_exists('test_table1', self.schema)
            db.create_table_if_not_exists('test_table2', self.schema)
            db.create_table_if_not_exists('test_table3', self.schema)

            assert db.table_exists('test_table1')
            assert db.table_exists('test_table2')
            assert db.table_exists('test_table3')

            db.remove_table('test_table1')
            db.remove_table('test_table2')
            db.remove_table('test_table3')

            assert not db.table_exists('test_table1')
            assert not db.table_exists('test_table2')
            assert not db.table_exists('test_table3')


