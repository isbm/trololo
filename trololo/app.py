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
from trololo.idmapper import TrololoIdMapper


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
        self._datamapper = None

    def _say_error(self, msg):
        """
        Print error message.

        :param msg:
        :return:
        """
        sys.stderr.write("\nError:\n  {}\n\n".format(msg))
        sys.exit(1)

    def _get_ids(self, argdata, section):
        """
        Get IDs or search for them in argument data.

        :param argdata: comma-separated ids or text.
        :return: list of ids
        """
        out = []
        if argdata is None:
            argdata = ""

        if " " in argdata:
            obj_id = self._datamapper.take_from(self._datamapper.get_id_by_name(argdata), section)
            if obj_id:
                out.append(obj_id)
        elif "," in argdata:
            # List of IDs, unless typo in the name
            for obj_id in self._client.get_arg_list(argdata):
                if self._datamapper.is_id(obj_id):
                    out.append(obj_id)
        elif self._datamapper.is_id(argdata):
            out.append(argdata)
        elif argdata:
            obj_id = self._datamapper.take_from(self._datamapper.get_id_by_name(argdata), section)
            if obj_id:
                out.append(obj_id)

        return out

    def board(self):
        """
        Operations with the boards.

        :return:
        """
        def show_labels(args):
            """
            Show labels.

            :param args:
            :return:
            """
            out = []
            boards = self._client.get_boards(*self._get_ids(args.labels, TrololoIdMapper.S_BOARD))
            for idx, board in enumerate(boards):
                idx += 1
                self._datamapper.add_board(board)
                out.append("{}. {}".format(str(idx).zfill(len(str(len(boards)))), board.name)[:80])
                labels = board.get_labels()
                if labels:
                    out.append("    \\__")
                for label in labels:
                    self._datamapper.add_label(label)
                    out.append('       "{}" ({})'.format(label.name, label.color))
                    out.append("       Id: {}".format(label.id))
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        def show_boards(args):
            """
            Show available boards.

            :param args:
            :return:
            """
            out = []
            boards = self._client.get_boards(*self._get_ids(args.display, TrololoIdMapper.S_BOARD))
            for idx, board in enumerate(boards):
                idx += 1
                self._datamapper.add_board(board)
                out.append("{}. {}".format(str(idx).zfill(len(str(len(boards)))), board.name)[:80])
                if board.desc:
                    out.append("    {}".format(board.desc)[:80])
                out.append("    Id: {}".format(board.id))
                if args.format == "expand":
                    lists = board.get_lists()
                    if lists:
                        out.append("    \\__")
                    for t_list in lists:
                        self._datamapper.add_list(t_list)
                        out.append('       "{}"'.format(t_list.name)[:80])
                        out.append("       Id: {}".format(t_list.id))
                out.append("-" * 80)
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        def show_board_map(args):
            """
            Display the entire board map.

            :param args:
            :return:
            """
            board_id = self._datamapper.take_from(self._datamapper.get_id_by_name(args.display), "boards")
            out = []
            ofs = " " * 4
            for board in self._client.get_boards(board_id):
                self._datamapper.add_board(board)
                out.extend(["{}".format(board.name), "=" * len(board.name)])
                lists = board.get_lists()
                if lists:
                    out.append(" \\__")
                for t_list in lists:
                    self._datamapper.add_list(t_list)
                    out.extend(["", "{}{}".format(ofs, t_list.name), "{}{}".format(ofs, "-" * len(t_list.name))])
                    cards = t_list.get_cards()
                    if cards:
                        out.append(" {}\\__".format(ofs))
                    for card in cards:
                        self._datamapper.add_card(card)
                        out.append("{}### {}".format(ofs * 2, card.name))
                        actions = card.get_actions()
                        if actions:
                            out.append(" {}\\__".format(ofs * 2))
                        for action in actions:
                            self._datamapper.add_action(action)
                            out.append("{}- {}".format(ofs * 3, action.get_text()))
                out.append("")
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        parser = argparse.ArgumentParser(description="operations with the boards")
        parser.add_argument("-s", "--show", help="show available boards", action="store_true")
        parser.add_argument("-f", "--format", help="choose what format to display",
                            choices=["short", "expand"], default="short")
        parser.add_argument("-d", "--display", help="show the entire map of the specific board. "
                                                    "Either pass an ID to display a board, "
                                                    "or pass a name of the board or a part of the name "
                                                    "(if you feeling lucky). WARNING: this can be lengthy!")
        parser.add_argument("-l", "--labels", help="specify ID of a Trello board to list its labels")
        parser.add_argument("-a", "--add", help="create a board", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.show and args.add:
            self._say_error("Should be either show boards or add one.")
        elif args.labels:
            show_labels(args)
        elif args.show:
            show_boards(args)
        elif args.add:
            raise NotImplementedError("Want to add boards? Edward would happily accept your PR on Trololo! :-P")
        elif args.display:
            show_board_map(args)
        else:
            parser.print_help()

    def list(self):
        """
        Operations with the Trello Lists in the board.

        :return:
        """

        def show_cards(args):
            """
            Show cards in the list.

            NOTE: This is duplicate functionality. The same can be achieved by "edward cards -l [list-id]".

            :param args:
            :return:
            """
            out = []
            for t_list in self._client.get_lists(*self._get_ids(args.show, TrololoIdMapper.S_LIST)):
                self._datamapper.add_list(t_list)
                out.extend([t_list.name, "=" * len(t_list.name)])
                cards = t_list.get_cards()
                if cards:
                    out.append("    \\__")
                    for idx, card in enumerate(cards):
                        self._datamapper.add_card(card)
                        idx += 1
                        out.append('       {}. "{}"'.format(str(idx).zfill(2), card.name)[:80])
                        out.append("       Id: {}".format(card.id))
                out.append("")
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        parser = argparse.ArgumentParser(description="operations with the Trello lists")
        parser.add_argument("-s", "--show", help="specify Trello list ID to display cards in it")
        parser.add_argument("-f", "--format", help="Choose what format to display",
                            choices=["short", "expand"], default="short")
        parser.add_argument("-a", "--add", help="add a list to the board", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        if args.show and args.add:
            self._say_error("Should be either display lists or add one.")
        elif args.show:
            show_cards(args)
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

        def show_cards(args):
            """
            Display cards in list.
            :return:
            """
            out = []
            for idx, t_list in enumerate(self._client.get_lists(*self._get_ids(args.list, TrololoIdMapper.S_LIST))):
                idx += 1
                self._datamapper.add_list(t_list)
                out.append('{}. "{}"'.format(idx, t_list.name))
                out.append("   Id: {}".format(t_list.id))
                cards = t_list.get_cards()
                if cards:
                    out.append("    \\__")
                for card in cards:
                    self._datamapper.add_card(card)
                    out.append('       "{}"'.format(card.name)[:80])
                    out.append("       Id: {}".format(card.id))
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        def show_comments(args):
            """
            Display comments in the card.

            :param args:
            :return:
            """
            out = []
            for idx, card in enumerate(self._client.get_cards(*self._get_ids(args.show, TrololoIdMapper.S_CARD))):
                idx += 1
                self._datamapper.add_card(card)
                out.append('{}  "{}"'.format(str(idx).zfill(2), card.name))
                out.append("    Id: {}".format(card.id))
                actions = card.get_actions()
                if actions:
                    out.append("    \\__")
                for action in actions:
                    self._datamapper.add_action(action)
                    out.append('       "{}"'.format(action.get_text())[:80])
                    out.append("       {}".format(action.date))
                    out.append("       Id: {}".format(action.id))
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        def add_card(args):
            """
            Add a card to the list.

            :param args:
            :return:
            """
            if not args.title:
                self._say_error("Title of the card is missing")
            elif not args.description:
                self._say_error("Description of the card is missing.\n  NOTE: It is not originally required by Trello.")
            out = []
            for t_list in self._client.get_lists(*self._get_ids(args.add, TrololoIdMapper.S_LIST)):
                out.append('New card has been added to "{}'.format(t_list.name)[:79] + '"')
                card = t_list.add_card(name=args.title, description=args.description)
                self._datamapper.add_card(card)
                if args.label:
                    print("Adding labels")
                    card.add_labels(*self._get_ids(args.label, TrololoIdMapper.S_LABEL))
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        def add_comment(args):
            """
            Add a comment to the card.

            :param args:
            :return:
            """
            out = []
            for card in self._client.get_cards(self._get_ids(args.card_id, TrololoIdMapper.S_CARD)):
                self._datamapper.add_card(card)
                new_comment = card.add_comment(args.comment)
                self._datamapper.add_action(new_comment)
                out.append("New comment has been added:")
                out.append("=" * len(out[0]))
                out.append("  {}".format(new_comment.get_text()))
            self._datamapper.save(bool(out))
            print(os.linesep.join(out))

        parser = argparse.ArgumentParser(description="operations with the cards in the Trello list",
                                         usage="edward card [-h] [-l] [-b] [-a] [-t]")
        parser.add_argument("-l", "--list", help="specify Trello list ID to display cards in it")
        parser.add_argument("-s", "--show", help="specify Trello Card ID to display comments in it")
        parser.add_argument("-b", "--list-labels", help="display cards with available labels", action="store_true")
        parser.add_argument("-a", "--add", help="specify Trello list ID to add a card to it")
        parser.add_argument("-i", "--card-id", help="specify Trello Card ID for modification", default=None)
        parser.add_argument("-c", "--comment", help="specify comment text for the card", default=None)
        parser.add_argument("-t", "--label", help="add a one or more labels to the card (comma-separated). "
                                                  "A label should contain a text and a color, separated by a "
                                                  "semi-colon. Example: 'my_label:red'")
        parser.add_argument("-e", "--title", help="title of the card.", default=None)
        parser.add_argument("-d", "--description", help="description/body of the card", default=None)
        args = parser.parse_args(sys.argv[2:])

        cli_st = len([_ for _ in [args.list, args.show, args.add, args.comment] if _]) - 1
        if cli_st > 0:
            parser.print_usage()
            self._say_error("Should you display cards in the list, comments in the card, or add a card.")
        elif cli_st < 0:
            parser.print_help()
            sys.exit(1)

        if args.list:
            show_cards(args)
        elif args.show:
            show_comments(args)
        elif args.add:
            add_card(args)
        elif args.card_id and args.comment:
            add_comment(args)

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
        self._datamapper = TrololoIdMapper("")

        m_ref(self)
