from comparison_dict import ComparisonDict
from db import Database, SchemaElement


class TestDatabase():
    schema = [
        SchemaElement(name='name', length=10, datatype='TEXT'),
        SchemaElement(name='valid', length=1, datatype='BOOLEAN'),
        SchemaElement(name='count', length=3, datatype='INTEGER')]

    data = [
        ["'Foonyor'", True, 1],
        ["'Barzane'", False, -12],
        ["'Quuxitude'", True, 103],
        ["'Foobar'", False, -3],
        ["'Foo2'", True, 999],
        ["'Foo3'", False, -1]]

    expected_list_of_dicts = [
        ComparisonDict([('name', 'Foonyor'), ('valid', '1'), ('count', 1)]),
        ComparisonDict([('name', 'Barzane'), ('valid', '0'), ('count', -12)]),
        ComparisonDict([('name', 'Quuxitude'), ('valid', '1'), ('count', 103)]),
        ComparisonDict([('name', 'Foobar'), ('valid', '0'), ('count', -3)]),
        ComparisonDict([('name', 'Foo2'), ('valid', '1'), ('count', 999)]),
        ComparisonDict([('name', 'Foo3'), ('valid', '0'), ('count', -1)])]

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

    def test_insert_rows(self):
        with Database() as db:
            db.create_table_if_not_exists('test_table1', self.schema)
            db.insert_rows('test_table1', self.schema, self.data)

            assert db.count_table_rows('test_table1') == 6
            db.remove_table('test_table1')
            assert not db.table_exists('test_table1')

    def test_fetch_all_as_dict(self):
        with Database() as db:
            db.create_table_if_not_exists('test_table1', self.schema)
            db.insert_rows('test_table1', self.schema, self.data)

            assert db.count_table_rows('test_table1') == 6
            test_dict = db.fetch_all_as_dict('test_table1')
            db.remove_table('test_table1')

            assert self.expected_list_of_dicts == test_dict

