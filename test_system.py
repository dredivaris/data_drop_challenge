import pytest
import subprocess


class TestParser:
    def test_parser_basic(self):
        # run command line parser
        successful_end = subprocess.call("./file_parser_daemon.py")
        assert successful_end == 0
        # create spec and data files
        # wait briefly
        # verify values in db
        # cleanup