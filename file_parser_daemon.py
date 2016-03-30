#!/usr/bin/env python
import os
from time import sleep

import cli.app
import sys

from parser import FileParser


@cli.app.CommandLineApp
def run_parser(app):
    if app.params.daemonize:
        # print("About to daemonize locally")
        file_parser = FileParser('data', 'specs')
        print('PID:', os.getpid())
        sys.stdout.flush()

        file_parser(one_pass=False)

    else:
        print('run one time')
        file_parser = FileParser('data', 'specs')
        file_parser()

run_parser.add_param("-d", "--daemonize", help="daemonize parser",
                     default=False, action="store_true")


# def run():
#     file_parser = FileParser('data', 'specs')
#     file_parser()

if __name__ == "__main__":
    # run()
    run_parser.run()
