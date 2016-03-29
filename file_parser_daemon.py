#!/usr/bin/env python
import cli.app

from parser import FileParser


@cli.app.CommandLineApp(reraise=None)
def run_parser(app):
    # if app.params.daemonize:
    #     app.log.info("About to daemonize")
    #     app.daemonize()

    file_parser = FileParser('data', 'specs')
    file_parser()

# run_parser.add_param("-d", "--daemonize", help="daemonize parser",
#                      default=False, action="store_true")


def run():
    file_parser = FileParser('data', 'specs')
    file_parser()

if __name__ == "__main__":
    run()
    # run_parser.run()
