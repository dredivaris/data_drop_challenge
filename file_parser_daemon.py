#!/usr/bin/env python
import cli.app

from parser import FileParser


@cli.app.CommandLineApp
def run_parser(app):
    # if app.params.daemonize:
    #     app.log.info("About to daemonize")
    #     app.daemonize()

    file_parser = FileParser('data', 'specs')
    file_parser()

run_parser.add_param("-d", "--daemonize", help="daemonize parser",
                     default=False, action="store_true")


if __name__ == "__main__":
    run_parser.run()