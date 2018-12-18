# coding=utf-8
"""
Lalala package contains main objects of Trello to work with.
"""

import re


class TrololoObject(object):
    """
    Interface for the Trololo objects.
    """
    _re_gr = re.compile(r"(.)([A-Z][a-z]+)")
    _re_sb = re.compile(r"([a-z0-9])([A-Z])")

    __attrs__ = []

    def _set_attrs(self, data):
        """
        :return:
        """
        for attr in self.__attrs__:
            setattr(self, self._uncamel(attr), data.get(attr))

    def _uncamel(self, name):
        """
        Convert "thisThing" to "this_thing".

        :param name:
        :return:
        """
        return self._re_sb.sub(r'\1_\2', self._re_gr.sub(r"\1_\2", name)).lower()

    @classmethod
    def load(cls, client, data):
        """
        Create an instsance from self.

        :param data:
        :return:
        """
        return cls(client, **data)


class TrololoCard(TrololoObject):
    """
    Trello card on the trello list of the board.
    """
    def __init__(self, client, **kwargs):
        self.__client = client

    def get_comments(self):
        """
        List comments (actions) of the cards.

        :return:
        """


class TrololoList(TrololoObject):
    """
    Trello list on the trello Board.
    """
    __attrs__ = ["id", "name", "closed", "idBoard"]

    def __init__(self, client, **kwargs):
        self.__client = client
        self._set_attrs(kwargs)

    def get_cards(self):
        """
        Get cards in the list.

        :return:
        """


class TrololoBoard(TrololoObject):
    """
    Trello Board.
    """
    __attrs__ = ["id", "name", "desc", "shortUrl", "url", "dateLastView"]

    def __init__(self, client, **kwargs):
        """
        :param client:
        :param id:
        :param name:
        """
        self.__client = client
        self._set_attrs(kwargs)

        self._trello_lists = []
        for list_obj in kwargs.get("lists", []):
            self._trello_lists.append(TrololoList.load(self.__client, list_obj))

    def get_lists(self):
        """
        Get lists.

        :return:
        """
        return self._trello_lists

    def get_cards(self, list_id):
        """
        List all cards.

        :return:
        """
