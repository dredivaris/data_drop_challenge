from os import listdir

from os.path import isfile, join
from time import sleep


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
        self._process_spec(spec_file)
        
        # 2) process data
        self._process_data(matching_data_file)

    def _process_spec(self, spec_file):
        pass

    def _process_data(self, matching_data_file):
        pass
