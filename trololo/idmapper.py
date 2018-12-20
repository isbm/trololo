"""
A very simple helper to operate Trello data by strings,
instead of remembering those cumbersome IDs.
"""

import pickle
import os
import sys

import trololo.exceptions
from trololo.lalala import TrololoBoard, TrololoAction, TrololoLabel, TrololoCard, TrololoList


class TrololoIdMapper(object):
    """
    Keeps on the disk what we already know.
    """

    DATA_MAPPER_FILE = "edward.bin"

    def __init__(self, path):
        """
        Path to the mapper storage.

        :param path:
        """
        self.__datamap = {
            "boards": {},
            "lists": {},
            "cards": {},
            "labels": {},
            "actions": {},
            "id": {},
        }
        self.__path = os.path.join(path, self.DATA_MAPPER_FILE)
        self.load()

    def add_board(self, board: TrololoBoard) -> None:
        """
        Add board

        :param board:
        :return:
        """
        self.__datamap["boards"].setdefault(board.name, set()).add(board.id)

    def add_list(self, t_list: TrololoList) -> None:
        """
        Add list

        :param t_list:
        :return:
        """
        self.__datamap["lists"].setdefault(t_list.name, set()).add(t_list.id)

    def add_card(self, card: TrololoCard) -> None:
        """
        Add card

        :param card:
        :return:
        """
        self.__datamap["cards"].setdefault(card.name, set()).add(card.id)

    def add_label(self, label: TrololoLabel) -> None:
        """
        Add label

        :param label:
        :return:
        """
        self.__datamap["labels"].setdefault(label.name, set()).add(label.id)

    def add_action(self, action: TrololoAction) -> None:
        """
        Add action

        :param action:
        :return:
        """
        self.__datamap["actions"].setdefault(action.get_text(), set()).add(action.id)

    def is_id(self, text):
        """
        Check if the text is actually an ID.

        :param text:
        :return:
        """
        try:
            int(text, 16)
            _id = True
        except (ValueError, TypeError):
            _id = False

        return _id

    def get_id_by_name(self, text):
        """
        Lookup data mapper for the text occurrences and find
        out what kind of IDs possibly can be there. Search
        works only from starting with or entire string.

        This is not super-optimal solution, but does the job.

        :param text:
        :return:
        """

        found = False
        ret = dict(zip(list(self.__datamap.keys()), [set() for _ in range(len(self.__datamap))]))
        if not self.is_id(text):
            for section in self.__datamap:
                for txt, ids in self.__datamap[section].items():
                    if txt.startswith(text):
                        ret[section].update(ids)
                        if len(ret[section]) > 1:
                            # Nope, try just IDs instead.
                            raise trololo.exceptions.DataMapperError("More than one ID references to the same text")
                        found = True
        else:
            ret["id"].add(text)
            found = True

        if not found:
            raise trololo.exceptions.DataMapperError("No corresponding ID has been found.")

        return ret

    def take_from(self, search_result, section):
        """
        Finds an ID from the search result by section.

        :param search_result:
        :return:
        """
        return (search_result.get("id") or search_result[section] or set(' ')).pop().strip()

    def save(self, skip=False):
        """
        Save data map to the disk.

        :param skip: Helper to avoid check every time if there is something to save.
        :return:
        """
        if not skip:
            try:
                with open(self.__path, "wb") as dmh:
                    pickle.dump(self.__datamap, dmh)
            except Exception as ex:
                raise trololo.exceptions.DataMapperError("Error while saving data map: {}".format(ex))

    def load(self):
        """
        Load data map from the disk.

        :return:
        """
        try:
            with open(self.__path, "rb") as dmh:
                self.__datamap = pickle.load(dmh)
        except Exception as ex:
            sys.stderr.write("Error while loading mapper: {}\n".format(ex))
