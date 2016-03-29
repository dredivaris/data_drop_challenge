import csv
from io import StringIO
from os import listdir

from os.path import isfile, join
from time import sleep

from db import SchemaElement, Database


class FileParser(object):
    def __init__(self, data_dir, specs_dir):
        self.data_dir = data_dir
        self.specs_dir = specs_dir

    def __call__(self, one_pass=True):
        while True:
            # get all spec files from dir
            spec_files = (f for f in listdir(self.specs_dir) if isfile(join(self.specs_dir, f)))
            data_files = [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f))]

            # for each spec file, if has matching datafile, process
            for file in spec_files:
                spec_prefix = file.split('.')[0]
                # if matching datafile
                if any((spec_prefix in f for f in data_files)):
                    self._process_files(spec_prefix, data_files)

            if one_pass:
                break
            else:
                # repeat every second
                sleep(1)

    def _process_files(self, spec, data_files):
        spec_file = '{dir}/{filename}.csv'.format(dir=self.specs_dir, filename=spec)

        # currently use simple implementation where only 1st datafile matching with spec file
        # is used.  Requirements mentioned spec/data pair so assuming a 1-1 file relationship
        def find_matching_filename(only_first=True):
            files = []
            for file in data_files:
                if spec in file:
                    if only_first:
                        return file
                    files.append(file)
            return files
        matching_data_file = '{dir}/{filename}'.format(
            dir=self.data_dir, filename=find_matching_filename())
        
        # for each pair, 1) process spec
        table_name, schema = self._process_spec(spec_file)
        
        # 2) process data
        prepped_data = self._parse_data(matching_data_file, schema)

        # print(prepped_data)

        # 3) enter into table
        self._enter_data(table_name, schema, prepped_data)

    def _process_spec(self, spec_file):
        print(spec_file)
        schema = []
        with open(spec_file) as csv_file:
            spec_reader = csv.reader(csv_file, delimiter=',')
            table_name = None
            for row in spec_reader:
                if not table_name:
                    table_name, width, datatype = row
                    if width != 'width' or datatype != 'datatype':
                        raise ValueError('Invalid CSV format')
                else:
                    name, length, type = row
                    schema.append(SchemaElement(name=name, length=int(length), datatype=type))
        return table_name, schema

    def _parse_data(self, matching_data_file, schema):
        data_rows = []
        with open(matching_data_file) as data_file:
            for line in data_file:
                row = []
                s = StringIO(line)
                for schema_item in schema:
                    raw_data = s.read(schema_item.length)
                    if schema_item.datatype == 'TEXT':
                        val = "'{}'".format(raw_data.strip())
                    elif schema_item.datatype == 'BOOLEAN':
                        val = bool(int(raw_data))
                    else:
                        val = int(raw_data)
                    row.append(val)
                data_rows.append(row)

        return data_rows

    def _enter_data(self, table_name, schema, prepped_data):
        with Database() as db:
            db.insert_rows(table_name, schema, prepped_data)


