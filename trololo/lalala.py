# coding=utf-8
"""
Lalala package contains main objects of Trello to work with.
"""

import re
from collections import OrderedDict


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
        Create an instance from self.

        :param data:
        :return:
        """
        return cls(client, **data)


class TrololoAction(TrololoObject):
    """
    Trello comment (action).
    """
    __attrs__ = ["id", "type", "date", "data"]

    def __init__(self, client, **kwargs):
        self.__client = client
        self._set_attrs(kwargs)

    def get_text(self):
        """
        Get comment's text.

        :return:
        """
        return self.data.get("text", "* empty *")


class TrololoCard(TrololoObject):
    """
    Trello card on the trello list of the board.
    """
    __attrs__ = ["id", "name", "url", "desc", "shortUrl", "dateLastActivity", "closed"]

    def __init__(self, client, **kwargs):
        self.__client = client
        self._set_attrs(kwargs)

    def get_actions(self):
        """
        List comments (actions) of the cards.

        :return:
        """
        actions = []
        obj, err = self.__client._request("cards/{}/actions".format(self.id))

        if obj:
            for action in obj:
                actions.append(TrololoAction.load(self.__client, action))

        return actions

    def add_comment(self, text):
        """
        Add a comment to this card.

        :param text:
        :return:
        """
        query = {
            "text": text
        }
        obj, err = self.__client._request("cards/{}/actions/comments".format(self.id), query=query, method="POST")
        return TrololoAction.load(self.__client, obj)


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
        query = {
            "filter": "open",
            "customFieldItems": "true"
        }

        cards = []
        obj, err = self.__client._request("lists/{}/cards".format(self.id), query=query)

        if obj:
            for card in obj:
                cards.append(TrololoCard.load(self.__client, card))

        return cards


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

        self._trello_lists = OrderedDict()
        for list_obj in kwargs.get("lists", []):
            t_list = TrololoList.load(self.__client, list_obj)
            self._trello_lists[t_list.id] = t_list

    def get_lists(self, *lists):
        """
        Get lists.

        :return:
        """
        return self._trello_lists.values()
