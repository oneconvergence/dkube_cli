#!/usr/bin/env python

"""Tests for `dkube_cli` package."""


import unittest
from click.testing import CliRunner

from dkube_cli import dkube_cli
from dkube_cli import cli


class TestDkube_cli(unittest.TestCase):
    """Tests for `dkube_cli` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'dkube_cli.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
