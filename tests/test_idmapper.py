# coding=utf-8
"""
Unit test for ID mapper
"""

import pytest
import yaml.parser
from unittest.mock import MagicMock, patch, mock_open

from trololo.idmapper import TrololoIdMapper
from trololo.lalala import TrololoBoard, TrololoList, TrololoCard, TrololoAction, TrololoLabel
import trololo.exceptions


class TestIDMapper(object):
    """
    Test ID mapper cases.
    """

    def test_first_init(self):
        """
        :return:
        """
        w_stderr = MagicMock()
        with patch("sys.stderr.write", w_stderr):
            TrololoIdMapper("/tmp")
            assert w_stderr.called
            assert "No such file or directory: '/tmp/edward.bin'" in w_stderr.call_args[0][0]

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_board(self):
        """
        Test board object is added and found.

        :return:
        """

        mapper = TrololoIdMapper("/tmp")
        mapper.add_board(TrololoBoard.load(None, {"id": "han_solo", "name": "Millennium Falcon"}))
        s_res = mapper.get_id_by_name("Millennium Falcon")

        assert s_res[TrololoIdMapper.S_BOARD].pop() == "han_solo"

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_list(self):
        """
        Test list object is added and found.

        :return:
        """

        mapper = TrololoIdMapper("/tmp")
        mapper.add_list(TrololoList.load(None, {"id": "dw_list", "name": "Darth Wader's visit list"}))
        s_res = mapper.get_id_by_name("Darth")  # Looking by the part of the name!

        assert s_res[TrololoIdMapper.S_LIST].pop() == "dw_list"

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_card(self):
        """
        Test card object is added and found.

        :return:
        """

        mapper = TrololoIdMapper("/tmp")
        mapper.add_card(TrololoCard.load(None, {"id": "leia_card", "name": "Princess Leia's visit card"}))
        s_res = mapper.get_id_by_name("Princess Leia")

        assert s_res[TrololoIdMapper.S_CARD].pop() == "leia_card"

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_action(self):
        """
        Test action object is added and found.

        :return:
        """

        mapper = TrololoIdMapper("/tmp")
        mapper.add_action(TrololoAction.load(None, {"id": "rrrawwwrrr", "data": {"text": "Chewbacca in action"}}))
        s_res = mapper.get_id_by_name("Chew")

        assert s_res[TrololoIdMapper.S_ACTION].pop() == "rrrawwwrrr"

