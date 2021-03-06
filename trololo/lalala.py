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

    def __init__(self, client, **kwargs):
        self._client = client
        self.__to_obj(kwargs)

    def __to_obj(self, data, obj=None):
        """
        JSON to object.

        :param data:
        :param obj:
        :return:
        """
        if obj is None:
            obj = self
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(obj, key, type(key, (), {}))
                self.__to_obj(value, getattr(obj, key))
            else:
                setattr(obj, key, value)

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


class TrololoLabel(TrololoObject):
    """
    Trello label on the board.
    """


class TrololoAction(TrololoObject):
    """
    Trello comment (action).
    """

    def get_text(self):
        """
        Get comment's text.

        :return:
        """
        return self.data.text


class TrololoCard(TrololoObject):
    """
    Trello card on the trello list of the board.
    """

    def get_actions(self):
        """
        List comments (actions) of the cards.

        :return:
        """
        actions = []
        for action in self._client._request("cards/{}/actions".format(self.id)):
            actions.append(TrololoAction.load(self._client, action))

        return actions

    def add_comment(self, text):
        """
        Add a comment to this card.

        :param text:
        :return:
        """
        return TrololoAction.load(self._client, self._client._request("cards/{}/actions/comments".format(self.id),
                                                                      query={"text": text}, method="POST"))

    def add_labels(self, *labels):
        """
        Add labels to this card.
        A labels is an array of key/value (text/color) dicts or TrololoLabel objects.

        :param labels:
        :return:
        """
        id_labels = []
        for label in labels:
            if isinstance(labels, TrololoLabel):
                id_labels.append(label.id)
            elif isinstance(label, str):
                id_labels.append(label)

        return TrololoLabel.load(self._client, self._client._request("cards/{}".format(self.id),
                                                                     query={"idLabels": ",".join(id_labels)},
                                                                     method="PUT"))


class TrololoList(TrololoObject):
    """
    Trello list on the trello Board.
    """

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
        for card in self._client._request("lists/{}/cards".format(self.id), query=query):
            cards.append(TrololoCard.load(self._client, card))

        return cards

    def add_card(self, name, description):
        """
        Add a card to this list.

        :param title:
        :param description:
        :param labels:
        :return:
        """
        query = {
            "idList": self.id,
            "keepFromSource": "all",
            "name": name,
            "desc": description,
            "pos": "top",
        }

        return TrololoCard.load(self._client, self._client._request("cards", query=query, method="POST"))


class TrololoBoard(TrololoObject):
    """
    Trello Board.
    """

    def get_lists(self):
        """
        Get lists.

        :return:
        """
        b_lists = []
        for list_obj in self.lists:
            t_list = TrololoList.load(self._client, list_obj)
            b_lists.append(t_list)

        return b_lists

    def get_labels(self):
        """
        Get labels.

        :return:
        """
        labels = []
        for b_obj in self._client._request("boards/{}/labels".format(self.id)):
            labels.append(TrololoLabel.load(self._client, b_obj))

        return labels
