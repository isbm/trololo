# coding=utf-8
"""
Unit test for ID mapper
"""

import pytest
import yaml.parser
from unittest.mock import MagicMock, patch, mock_open

from trololo.idmapper import TrololoIdMapper
from trololo.lalala import TrololoBoard
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

