from time import sleep

import pytest
import subprocess

from datetime import date

from db import Database


class TestParser:

    def compare_test_data(self, input_dict, response_dict):
        if input_dict.keys() != response_dict.keys():
            return False
        for key in input_dict.keys():
            if str(input_dict[key]).strip() != str(response_dict[key]).strip():
                return False
        return True

    def test_parser_basic(self):
        # run command line parser
        successful_end = subprocess.call("./file_parser_daemon.py")
        assert successful_end == 0

        # create spec and data files
        with open('specs/testformat1.csv', 'w') as f:
            f.write('test1,width,datatype\nname,10,TEXT\nvalid,1,BOOLEAN\ncount,3,INTEGER')

        today = date.today().strftime('%Y-%m-%d')
        # generate date
        expected_data = [
            {'name': 'Foonyor   ', 'valid': '1', 'count': '  1'},
            {'name': 'Barzane   ', 'valid': '0', 'count': '-12'},
            {'name': 'Quuxitude ', 'valid': '1', 'count': '103'},
        ]
        with open('data/testformat1_{dt}.txt'.format(dt=today), 'w') as f:
            for line in expected_data:
                f.write('{name}{valid}{count}\n'.format(name=line['name'],
                                                        valid=line['valid'],
                                                        count=line['count']))
        sleep(.1)

        # verify values in db
        # with Database() as db:
        #     all_rows = db.fetchall('test1')
        #     for row in all_rows:
                
                
            # use package_obj

        # cleanup