"""
A very simple helper to operate Trello data by strings,
instead of remembering those cumbersome IDs.
"""

import pickle
import os

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
        }
        self.__path = os.path.join(path, self.DATA_MAPPER_FILE)

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
        self.__datamap["actions"].setdefault(action.name, set()).add(action.id)

    def get_id_by_name(self, text):
        """
        Lookup data mapper for the text occurrences and find
        out what kind of IDs possibly can be there. Search
        works only from starting with or entire string.

        This is not super-optimal solution, but does the job.

        :param text:
        :return:
        """
        try:
            int(text, 16)
            is_id = True
        except (ValueError, TypeError):
            is_id = False

        found = False
        ret = dict(zip(list(self.__datamap.keys()) + ["id"], [set() for _ in range(len(self.__datamap))]))
        if not is_id:
            for section in self.__datamap:
                for txt, ids in section.items():
                    if txt.startswith(text):
                        ret[section].update(ids)
                        found = True
        else:
            ret["id"].add(text)

        if not found:
            raise trololo.exceptions.DataMapperError("No corresponding ID has been found.")

        return ret

    def save(self):
        """
        Save data map to the disk.

        :return:
        """
        try:
            with open(self.__path, "w") as dmh:
                pickle.dump(dmh, self.__datamap)
        except Exception as ex:
            raise trololo.exceptions.DataMapperError("Error while saving data map: {}".format(ex))

    def load(self):
        """
        Load data map from the disk.

        :return:
        """
        try:
            with open(self.__path, "r") as dmh:
                self.__datamap = pickle.load(dmh)
        except Exception as ex:
            raise trololo.exceptions.DataMapperError("Error while loading data map: {}".format(ex))
