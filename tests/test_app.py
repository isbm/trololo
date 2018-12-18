# coding=utf-8
"""
Unit tests for App
"""

import pytest
from unittest.mock import MagicMock, patch

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
    def test_runner_raises_on_config_absent(self, app):
        """
        Test if runner raises an exception, once configuration is not found.

        :return:
        """
        with pytest.raises(trololo.exceptions.CLIError) as ex:
            app.run()

        assert "Configuration file 'edward.conf' is not found in the current directory." in str(ex)
