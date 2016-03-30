import os
import subprocess
from datetime import date
from time import sleep

import psutil as psutil

from comparison_dict import ComparisonDict
from db import Database

class ParserTestData:
    schema_a = ['test1,width,datatype', 'name,10,TEXT', 'valid,1,BOOLEAN', 'count,3,INTEGER']
    expected_data_a = [
        ComparisonDict((('name', 'Foonyor   '), ('valid', '1'), ('count', '  1'))),
        ComparisonDict((('name', 'Barzane   '), ('valid', '0'), ('count', '-12'))),
        ComparisonDict((('name', 'Quuxitude '), ('valid', '1'), ('count', '103'))),
        ComparisonDict((('name', 'Foobar    '), ('valid', '0'), ('count', ' -3'))),
        ComparisonDict((('name', 'Foo2      '), ('valid', '1'), ('count', '999'))),
        ComparisonDict((('name', 'Foo3      '), ('valid', '0'), ('count', ' -1')))
    ]

    schema_b = [
        'test3,width,datatype',
        'size,3,INTEGER',
        'weight,3,INTEGER',
        'model,8,TEXT',
        'make,7,TEXT',
        'stock,1,BOOLEAN'
    ]
    expected_data_b = [
        ComparisonDict(
            (('size', '234'), ('weight', ' 23'), ('model', 'sentra  '),
             ('make', 'nissan '), ('stock', '0'))),
        ComparisonDict(
            (('size', ' 94'), ('weight', '  9'), ('model', 'cruze   '),
             ('make', 'chevy  '), ('stock', '1'))),
        ComparisonDict(
            (('size', '934'), ('weight', '612'), ('model', 'F-350   '),
             ('make', 'ford   '), ('stock', '1')))
    ]

    @staticmethod
    def _schema_to_csv_string(schema):
        return '\n'.join(schema)

    @staticmethod
    def _remove_test_tables(self, *args):
        with Database() as db:
            for arg in args:
                db.remove_table(arg)



    @staticmethod
    def _create_files():
        pass


class TestParserOneTime(ParserTestData):
    def test_parser_basic(self):
        try:
            today = date.today().strftime('%Y-%m-%d')
            specsfile = 'specs/testformat1.csv'
            datafile = 'data/testformat1_{dt}.txt'.format(dt=today)

            # create spec and data files
            with open(specsfile, 'w') as f:

                f.write(TestParserOneTime._schema_to_csv_string(self.schema_a))

            with open(datafile, 'w') as f:
                for line in self.expected_data_a:
                    f.write('{name}{valid}{count}\n'.format(name=line['name'],
                                                            valid=line['valid'],
                                                            count=line['count']))
            sleep(.1)

            # run app
            successful_end = subprocess.call("./file_parser_daemon.py")
            assert successful_end == 0

            # verify values in db
            with Database() as db:
                all_rows = db.fetch_all_as_dict('test1')
                for row in all_rows:
                    assert row in self.expected_data_a
        finally:
            # cleanup
            try:
                os.remove(specsfile)
                os.remove(datafile)
                self._remove_test_tables('test1')
            except:
                pass

    # test 3 files of 2 rows each, same schema as above
    def test_parser_multiple_files(self):
        today = date.today().strftime('%Y-%m-%d')
        name = 'test_format'
        expected = list(self.expected_data_a)
        # setup data files
        try:
            for i in range(3):
                specsfile = 'specs/{}{}.csv'.format(name, i)
                datafile = 'data/{}{}_{dt}.txt'.format(name, i, dt=today)

                # create spec and data files
                with open(specsfile, 'w') as f:
                    f.write('test1,width,datatype\nname,10,TEXT\nvalid,1,BOOLEAN\ncount,3,INTEGER')

                with open(datafile, 'w') as f:
                    data_for_this_file = [expected.pop(), expected.pop()]
                    for line in data_for_this_file:
                        f.write('{name}{valid}{count}\n'.format(name=line['name'],
                                                                valid=line['valid'],
                                                                count=line['count']))
                sleep(.1)

            # run app
            successful_end = subprocess.call("./file_parser_daemon.py")
            assert successful_end == 0

            # verify values in db
            with Database() as db:
                all_rows = db.fetch_all_as_dict('test1')
                for row in all_rows:
                    assert row in self.expected_data_a
        finally:
            # cleanup
            try:
                for i in range(3):
                    specsfile = 'specs/{}{}.csv'.format(name, i)
                    datafile = 'data/{}{}_{dt}.txt'.format(name, i, dt=today)
                    os.remove(specsfile)
                    os.remove(datafile)
                    self._remove_test_tables('test1')
            except:
                pass

    def test_larger_schema(self):
        try:
            today = date.today().strftime('%Y-%m-%d')
            specsfile = 'specs/testformat_b.csv'
            datafile = 'data/testformat_b_{dt}.txt'.format(dt=today)

            # create spec and data files
            with open(specsfile, 'w') as f:

                f.write(TestParserOneTime._schema_to_csv_string(self.schema_b))

            with open(datafile, 'w') as f:
                for line in self.expected_data_b:
                    print(line.values())
                    f.write('{}\n'.format(''.join(line.values())))
                    # f.write('{name}{valid}{count}\n'.format(name=line['name'],
                    #                                         valid=line['valid'],
                    #                                         count=line['count']))
            sleep(.1)

            # run app
            successful_end = subprocess.call("./file_parser_daemon.py")
            assert successful_end == 0

            # verify values in db
            with Database() as db:
                all_rows = db.fetch_all_as_dict('test3')
                for row in all_rows:
                    assert row in self.expected_data_b
        finally:
            # cleanup
            try:
                os.remove(specsfile)
                os.remove(datafile)
                self._remove_test_tables('test3')
            except:
                pass


class TestParserAsDaemon(ParserTestData):
    def test_parser_continuous_basic(self):
        # successful_end = subprocess.call(["./file_parser_daemon.py", "-d"])
        # successful_end = subprocess.call("./file_parser_daemon.py -d")

        args = ["python", "file_parser_daemon.py", "-d"]
        # start process before dumping files
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        pid_bytes = proc.stdout.readline()
        pid = int(pid_bytes.decode("utf-8").split(': ')[1].strip())

        sleep(.5)

        # place files in directory to be processed
        try:
            today = date.today().strftime('%Y-%m-%d')
            specsfile = 'specs/testformat1.csv'
            datafile = 'data/testformat1_{dt}.txt'.format(dt=today)

            # create spec and data files
            with open(specsfile, 'w') as f:

                f.write(TestParserOneTime._schema_to_csv_string(self.schema_a))

            with open(datafile, 'w') as f:
                for line in self.expected_data_a:
                    f.write('{name}{valid}{count}\n'.format(name=line['name'],
                                                            valid=line['valid'],
                                                            count=line['count']))
            sleep(.5)

            # verify values in db
            with Database() as db:
                all_rows = db.fetch_all_as_dict('test1')
                for row in all_rows:
                    assert row in self.expected_data_a

        finally:
            # cleanup
            try:
                os.remove(specsfile)
                os.remove(datafile)
                self._remove_test_tables('test1')
            except:
                pass

            psutil.Process(pid).terminate()
