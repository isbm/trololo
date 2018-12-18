# coding=utf-8

"""
CLI app.
"""

import argparse
import sys
import os
import yaml

import trololo.exceptions

class TrololoApp(object):
    """
    Trololo CLI application.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Edward performs simple operations on Trello board.",
                                              usage="""edward <command> [<args>]
Available commands are:
    board    Operations with the boards on Trello.
    column   Operations with the columns of specific board.
    card     Operations with the cards of specific column on the board.

""")
        self.parser.add_argument("command", help="Subcommand to run")
        self.cli_args = self.parser.parse_args(sys.argv[1:2])
        self.config = {}
        self._client = None

    def _say_error(self, msg):
        """
        Print error message.

        :param msg:
        :return:
        """
        sys.stderr.write("\nError:\n  {}\n\n".format(msg))
        sys.exit(1)

    def board(self):
        """
        Operations with the boards.

        :return:
        """
        parser = argparse.ArgumentParser(description="operations with the boards")
        parser.add_argument("-l", "--list", help="List available boards", action="store_true")
        parser.add_argument("-a", "--add", help="Create a board", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.list and args.add:
            self._say_error("Should be either list boards or add one.")

    def column(self):
        """
        Operations with the columns in the board.

        :return:
        """
        parser = argparse.ArgumentParser(description="operations with the columns")
        parser.add_argument("-l", "--list", help="List columns in the board", action="store_true")
        parser.add_argument("-a", "--add", help="Add a column to the board", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.list and args.add:
            self._say_error("Should be either list columns or add one.")

    def card(self):
        """
        Operations with the cards in the column.

        :return:
        """
        parser = argparse.ArgumentParser(description="operations with the cards in the column",
                                         usage="edward card [-h] [-l] [-b] [-a] [-t]")
        parser.add_argument("-l", "--list", help="List cards in the specified column", action="store_true")
        parser.add_argument("-b", "--list-labels", help="List available labels of the card", action="store_true")
        parser.add_argument("-a", "--add", help="Add a card", action="store_true")
        parser.add_argument("-t", "--label", help="Add a one or more labels to the card (comma-separated)",
                            action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.list and args.add:
            self._say_error("Should be either list boards or add one.")
        elif not args.list and not args.add:
            parser.print_usage()
            sys.exit(1)

    def run(self):
        """
        Run CLI app.

        :return:
        """
        cfg_file = "edward.conf"
        if not os.path.exists(cfg_file):
            raise trololo.exceptions.CLIError(
                "Configuration file '{}' is not found in the current directory.".format(cfg_file))

        with open(cfg_file) as cfg_h:
            self.config = yaml.load(cfg_h)

        m_ref = self.__class__.__dict__.get(self.cli_args.command)
        if m_ref is None:
            sys.stderr.write("Unknown command: {}\n\n".format(self.cli_args.command))
            self.parser.print_help()
            sys.exit(os.EX_USAGE)

        self._client = TrololoClient(**self.config)

        m_ref(self)
