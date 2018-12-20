# coding=utf-8
"""
Unit test for ID mapper
"""

import pytest
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

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_plain_id(self):
        """
        Test id found.

        :return:
        """

        mapper = TrololoIdMapper("/tmp")
        s_res = mapper.get_id_by_name("deadbeef")

        assert s_res[TrololoIdMapper.S_ID].pop() == "deadbeef"

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_plain_id_not_found(self):
        """
        Test id not found, if it is not a number.

        :return:
        """

        with pytest.raises(trololo.exceptions.DataMapperError) as ex:
            TrololoIdMapper("/tmp").get_id_by_name("solaris")

        assert "No corresponding ID has been found" in str(ex)

    @patch("sys.stderr.write", MagicMock())
    def test_add_find_label(self):
        """
        Test label object is added and found.

        :return:
        """

        mapper = TrololoIdMapper("/tmp")
        mapper.add_label(TrololoLabel.load(None, {"id": "splat", "name": "Star Wars"}))
        s_res = mapper.get_id_by_name("Star Wars")

        assert s_res[TrololoIdMapper.S_LABEL].pop() == "splat"

    @patch("sys.stderr.write", MagicMock())
    def test_add_is_id(self):
        """
        Test is_id function

        :return:
        """

        assert TrololoIdMapper.is_id("deadbeef")
        assert not TrololoIdMapper.is_id("disks spinning backwards - toggle the hemisphere jumper")

    @patch("sys.stderr.write", MagicMock())
    @patch("trololo.idmapper.open", mock_open(), create=True)
    def test_save_dump(self):
        """
        Test save.

        :return:
        """
        _name = "Loop in redundant loopback"
        _id = "networking"
        mapper = TrololoIdMapper("/tmp")
        mapper.add_board(TrololoBoard.load(None, {"id": _id, "name": _name}))
        dumper = MagicMock()
        with patch("pickle.dump", dumper):
            mapper.save()
            assert dumper.called
            assert dumper.call_args[0][0][TrololoIdMapper.S_BOARD].get(_name).pop() == _id

    @patch("sys.stderr.write", MagicMock())
    @patch("trololo.idmapper.open", mock_open(), create=True)
    @patch("pickle.dump", MagicMock(side_effect=IOError("Electricians made popcorn in the power supply")))
    def test_save_dump_failure(self):
        """
        Test save failure.

        :return:
        """

        with pytest.raises(Exception) as ex:
            TrololoIdMapper("/tmp").save()
        assert "popcorn" in str(ex)
