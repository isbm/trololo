# coding=utf-8
"""
Lalala package contains main objects of Trello to work with.
"""


class TrololoObject(object):
    """
    Interface for the Trololo objects.
    """

    @staticmethod
    def load(client, data):
        """
        Load board from the JSON data.

        :param client: Client instance
        :param data: JSON data
        :return: Implemented Element object
        """
        raise NotImplementedError("Loading not implemented")

