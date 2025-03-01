#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from imessage_reader import cli


@pytest.fixture()
def create_parser():
    """
    Create a parser
    """
    parser = cli.get_parser()
    yield parser


def test_evaluate(create_parser):
    """
    Test if the given arguments will be parsed.
    :param create_parser: The created parser
    """
    args_version = create_parser.parse_args(["--version"])
    args_recipients = create_parser.parse_args(["--recipients"])
    args_output = create_parser.parse_args(["--output"])
    args_contact = create_parser.parse_args(["--contact", "+1234567890"])

    assert args_version.version is True
    assert args_recipients.recipients is True
    assert args_output.output is None
    assert args_contact.contact == "+1234567890"


def test_check_database_path(mocker):
    # Test without contact filter
    mocker.patch(
        "sys.argv",
        [
            "imessage_reader",
            "--path",
            "/Users/bodo/Documents",
            "--output",
            "e"
        ],
    )

    args = cli.get_parser().parse_args()
    assert args.path == "/Users/bodo/Documents"
    assert args.output == "e"
    assert args.recipients is False
    assert args.version is False
    assert args.contact is None

    # Test with contact filter
    mocker.patch(
        "sys.argv",
        [
            "imessage_reader",
            "--path",
            "/Users/bodo/Documents",
            "--contact",
            "+1234567890"
        ],
    )

    args = cli.get_parser().parse_args()
    assert args.path == "/Users/bodo/Documents"
    assert args.contact == "+1234567890"
