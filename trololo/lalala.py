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


    @staticmethod
    def load(client, data):
        """
        Load board from the JSON data.
    def _uncamel(self, name):
        """
        Convert "thisThing" to "this_thing".

        :param name:
        :return:
        """
        return self._re_sb.sub(r'\1_\2', self._re_gr.sub(r"\1_\2", name)).lower()

        :param client: Client instance
        :param data: JSON data
        :return: Implemented Element object
        """
        raise NotImplementedError("Loading not implemented")


class TrololoBoard(TrololoObject):
    """
    Trello Board.
    """
    def __init__(self, client, **kwargs):
        """
        :param client:
        :param id:
        :param name:
        """
        self.__client = client
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.descr = kwargs.get("desc")
        self.link = kwargs.get("shortUrl")
        self.url = kwargs.get("url")
        self.last_viewed = kwargs.get("dateLastView")

    def list_cards(self):
        """
        List all cards.

        :return:
        """

    @staticmethod
    def load(client, data):
        """
        Create board object instance from JSON.

        :param client: Client instance
        :param data: JSON data
        :return: TrololoBoard object
        """
        return TrololoBoard(client=client, **data)
