# coding=utf-8

"""
Network client implementation.
"""

import sys
import http
import requests
import urllib.parse

from trololo.lalala import TrololoBoard
from trololo import exceptions


class Trololo(object):
    """
    Trololo client.
    """
    def __init__(self, key, token):
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
            obj, err = response.json(), None
        except Exception as ex:
            sys.stderr.write("JSON error: {}\n".format(ex))
            obj, err = None, response.text

        return obj, err


class TrololoClient(Trololo):
    """
    Client example.
    """
    def list_boards(self):
        """
        List available boards.

        :return:
        """
        query = {
            "filter": "all",
            "fields": "all",
            "lists": "none",
            "memberships": "none",
            "organization": "false",
            "organization_fields": "name,displayName",
        }
        obj, err = self._request("members/the_bofh/boards", query=query)
        boards = []
        if obj is not None:
            for board_json in obj:
                boards.append(TrololoBoard.load(self, board_json))

        return boards
