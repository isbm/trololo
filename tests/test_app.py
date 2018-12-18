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

    @patch("trololo.app.TrololoClient", MagicMock())
    def test_unknown_command_failure(self, app):
        """
        Test if runner fails with the STDERR of the unknown command.

        :param app:
        :return:
        """
        err_msg = "We only support 14400 bps connection"
        app.cli_args = MagicMock()
        app.cli_args.command = "bazinga"
        stderr = MagicMock()
        with patch("trololo.app.open", mock_open(read_data="foo: bar"), create=True):
            exit = MagicMock(side_effect=Exception(err_msg))
            with patch("sys.exit", exit):
                with patch("sys.stderr.write", stderr):
                    with pytest.raises(Exception) as ex:
                        app.run()
                    assert err_msg in str(ex)
                    assert stderr.called
                    assert "Unknown command: {}".format(app.cli_args.command) in stderr.call_args[0][0]

    @patch("sys.exit", MagicMock())
    def test_error_output(self, app):
        """
        Test error output is up to format.

        :param app:
        :return:
        """
        err_msg = "Magnetic interference from Van Allen Belt"
        stderr = MagicMock()
        with patch("sys.stderr.write", stderr):
            app._say_error(err_msg)
            assert stderr.called
            assert err_msg in stderr.call_args[0][0]
            assert "\nError:\n  {}\n\n".format(err_msg) == stderr.call_args[0][0]
