# coding=utf-8

"""
Network client implementation.
"""

import sys
import http
import requests
import urllib.parse

from trololo.lalala import TrololoBoard, TrololoList, TrololoCard
from trololo import exceptions


class Trololo(object):
    """
    Trololo client.
    """
    def __init__(self, uid, key, token):
        self._api_uid = uid
        self._api_key = key
        self._api_token = token
        self._api_root_url = "https://api.trello.com/1/"

    def _request(self, uri, query=None, method="GET"):
        """
        Generic request to the Trello.

        :param uri:
        :return:
        """
        params = {
            "key": self._api_key,
            "token": self._api_token
        }

        params.update(query or {})

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json"
        }
        url = urllib.parse.urljoin(self._api_root_url, uri.lstrip("/"))
        response = requests.request(method, url, params=params, headers=headers)

        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            raise exceptions.UnauthorisedError("{} for {}".format(response.text, url))
        elif response.status_code != http.HTTPStatus.OK:
            raise exceptions.UnknownResourceError("{} at {}".format(response.text, url))

        try:
            obj = response.json()
        except Exception as ex:
            sys.stderr.write("JSON error: {}\n".format(ex))
            sys.stderr.write("\n--- response / trace ---\n")
            sys.stderr.write(response.text)
            sys.stderr.write("\n------------------------\n\n")

            raise exceptions.RequestError("Oops... Looks like we're done at the moment. Look above.")

        return obj


class TrololoClient(Trololo):
    """
    Client example.
    """
    @staticmethod
    def get_arg_list(arg):
        """
        Converts comma-separated values into the list.

        :param arg:
        :return:
        """
        if not arg:
            out = []
        elif "," in arg:
            out = [item for item in arg.split(",") if item.strip()]
        else:
            out = [arg]

        return out

    def get_boards(self, *ids):
        """
        List available boards.

        :return:
        """
        query = {
            "filter": "all",
            "fields": "all",
            "lists": "open",
            "memberships": "none",
            "organization": "false",
            "organization_fields": "name,displayName",
        }
        obj, err = self._request("members/{}/boards".format(self._api_uid), query=query)
        boards = []
        if obj is not None:
            for board_json in obj:
                board = TrololoBoard.load(self, board_json)
                if ids and board.id in ids or not ids:
                    boards.append(board)

        return boards

    def get_lists(self, *ids):
        """
        Get lists by IDs.

        :param ids:
        :return:
        """
        query = {
            "fields": "name,closed,idBoard"
        }

        lists = []
        for list_id in ids:
            obj, err = self._request("lists/{}".format(list_id), query=query)
            if obj is not None:
                lists.append(TrololoList.load(self, obj))

        return lists

    def get_cards(self, *ids):
        """
        Get cards by list IDs.

        :param ids:
        :return:
        """
        query = {
            "filter": "open",
            "customFieldItems": "true"
        }

        cards = []
        for card_id in ids:
            obj, err = self._request("cards/{}".format(card_id), query=query)
            if obj:
                cards.append(TrololoCard.load(self, obj))

        return cards
