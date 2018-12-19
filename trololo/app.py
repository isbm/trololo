# coding=utf-8

"""
CLI app.
"""

import argparse
import sys
import os
import yaml

import trololo.exceptions
from trololo.client import TrololoClient


class TrololoApp(object):
    """
    Trololo CLI application.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Edward performs simple operations on Trello board.",
                                              usage="""edward <command> [<args>]
Available commands are:
    board    Operations with the boards on Trello.
    list     Operations with the lists of specific board.
    card     Operations with the cards of specific list on the board.

""")
        self.parser.add_argument("command", help="Subcommand to run", choices=["board", "list", "card"])
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
        parser.add_argument("-s", "--show", help="Show available boards", action="store_true")
        parser.add_argument("-f", "--format", help="Choose what format to display",
                            choices=["short", "expand"], default="short")
        parser.add_argument("-d", "--display", help="Show only specific board(s). Values are comma-separated.")
        parser.add_argument("-a", "--add", help="Create a board", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.show and args.add:
            self._say_error("Should be either show boards or add one.")
        elif args.show:
            out = []
            boards = self._client.list_boards(*self._client.get_arg_list(args.display))
            for idx, board in enumerate(boards):
                idx += 1
                out.append("{}. {}".format(str(idx).zfill(len(str(len(boards)))), board.name)[:80])
                if board.desc:
                    out.append("    {}".format(board.desc)[:80])
                out.append("    Id: {}".format(board.id))
                if args.format == "expand":
                    lists = board.get_lists()
                    if lists:
                        out.append("    \\__")
                    for list in lists:
                        out.append('       "{}"'.format(list.name)[:80])
                        out.append("       Id: {}".format(list.id))
                out.append("-" * 80)
            print(os.linesep.join(out))
        elif args.add:
            raise NotImplementedError("Want to add boards? Edward would happily accept "
                                      "your PR on Trololo! :-P")
        else:
            parser.print_help()

    def list(self):
        """
        Operations with the Trello Lists in the board.

        :return:
        """
        parser = argparse.ArgumentParser(description="operations with the Trello lists")
        parser.add_argument("-s", "--show", help="specify board ID to display Trello lists in it")
        parser.add_argument("-a", "--add", help="add a list to the board", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.show and args.add:
            self._say_error("Should be either display lists or add one.")
        elif args.show:
            boards = self._client.list_boards(*self._client.get_arg_list(args.show))
            if boards:
                out = []
                for board in boards:
                    out.extend([board.name, "=" * len(board.name)])
                    for idx, t_list in enumerate(board.get_lists()):
                        idx += 1
                        out.append("{}. {}".format(idx, t_list.name))
                    out.append("")
                print(os.linesep.join(out))
            else:
                raise trololo.exceptions.CLIError("Board with ID '{}' was not found.".format(args.show))
        elif args.add:
            raise NotImplementedError("Want to add lists to your boards? Sure thing! "
                                      "Edward would happily accept your PR on Trololo! :-P")
        else:
            parser.print_help()

    def card(self):
        """
        Operations with the cards in the Trello List.

        :return:
        """
        parser = argparse.ArgumentParser(description="operations with the cards in the Trello list",
                                         usage="edward card [-h] [-l] [-b] [-a] [-t]")
        parser.add_argument("-s", "--show", help="Specify Trello list ID to display cards in it")
        parser.add_argument("-b", "--list-labels", help="display cards with available labels", action="store_true")
        parser.add_argument("-a", "--add", help="add a card", action="store_true")
        parser.add_argument("-t", "--label", help="add a one or more labels to the card (comma-separated)",
                            action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.show and args.add:
            self._say_error("Should be either list boards or add one.")
        elif not args.show and not args.add:
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
