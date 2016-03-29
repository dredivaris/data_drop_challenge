import pytest
import subprocess


class TestParser:
    def test_parser_basic(self):
        # run command line parser
        successful_end = subprocess.call("./file_parser_daemon.py")
        assert successful_end == 0

        # create spec and data files
        with open('testformat1.csv', 'w') as f:
            f.write('test1,width,datatype')
            f.write('name,10,TEXT')
            f.write('valid,1,BOOLEAN')
            f.write('count,3,INTEGER')

        # generate date
        with open('testformat1_2015-06-28.txt', 'w') as f:
            f.write('test1,width,datatype')
            f.write('name,10,TEXT')
            f.write('valid,1,BOOLEAN')
            f.write('count,3,INTEGER')

        # wait briefly
        # verify values in db
        # cleanup