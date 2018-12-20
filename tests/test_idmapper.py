# coding=utf-8
"""
Unit test for ID mapper
"""

import pytest
import yaml.parser
from unittest.mock import MagicMock, patch, mock_open

from trololo.idmapper import TrololoIdMapper
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
