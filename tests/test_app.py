# coding=utf-8
"""
Unit tests for App
"""

import pytest
import yaml.parser
from unittest.mock import MagicMock, patch, mock_open

from trololo.app import TrololoApp
import trololo.exceptions


@pytest.fixture
@patch("argparse.ArgumentParser", MagicMock())
def app():
    """
    Return app instance

    :return:
    """

    return TrololoApp()


class TestTrololoApp(object):
    """
    Test application functionality unit tests.
    """
    @patch("os.path.exists", MagicMock(return_value=False))
    def test_exception_on_config_notfound(self, app):
        """
        Test if runner raises an exception, once configuration is not found.

        :return:
        """
        with pytest.raises(trololo.exceptions.CLIError) as ex:
            app.run()

        assert "Configuration file 'edward.conf' is not found in the current directory." in str(ex)

    def test_exception_on_config_failure(self, app):
        """
        Test if runner raises an exception, once configuration is wrong.

        :param app:
        :return:
        """
        with patch("trololo.app.open", mock_open(read_data="non-redundant\n: fan failure"), create=True):
            with pytest.raises(yaml.parser.ParserError) as ex:
                app.run()
            assert "expected '<document start>', but found '<block mapping start>'" in str(ex)
