"""
Tests for the cmdline tools.
"""
import pytest

from rawnicorn.cmdline import cmdline_parser


def test_cmdline_parser_should_raise_sysexit2_when_no_args_are_supplied():
    # act
    with pytest.raises(SystemExit) as exception:
        cmdline_parser.parse_args([])

    assert exception.type == SystemExit
    assert exception.value.code == 2


def test_cmdline_parser_should_raise_errors_when_log_level_options_are_not_respected():
    # act
    with pytest.raises(SystemExit) as exception:
        cmdline_parser.parse_args(["--host", "localhost", "--port", "8080", "--log-level", "unknown"])

    assert exception.type == SystemExit
    assert exception.value.code == 2


def test_cmdline_parser_should_raise_errors_when_log_level_options_are_not_respected_due_to_lowercase():
    # act
    with pytest.raises(SystemExit) as exception:
        cmdline_parser.parse_args(["--host", "localhost", "--port", "8080", "--log-level", "info"])

    assert exception.type == SystemExit
    assert exception.value.code == 2


def test_cmdline_parser_should_parse_values_with_defaults():
    # act
    parsed_args = cmdline_parser.parse_args(["--host", "localhost", "--port", "8080"])

    # assert
    assert parsed_args.host == "localhost"
    assert parsed_args.port == 8080
    assert parsed_args.workers == 1
    assert parsed_args.threads == 1
    assert parsed_args.log_level == "INFO"


def test_cmdline_parser_should_parse_values_without_all_defaults():
    # act
    parsed_args = cmdline_parser.parse_args(
        ["--host", "localhost", "--port", "8080", "--workers", "5", "--log-level", "WARNING"]
    )

    # assert
    assert parsed_args.host == "localhost"
    assert parsed_args.port == 8080
    assert parsed_args.workers == 5
    assert parsed_args.threads == 1
    assert parsed_args.log_level == "WARNING"
