import json
import unittest

from looqbox.utils.utils import _format_quotes


class TestFormatQuotes(unittest.TestCase):
    def test_single_backslash(self):
        input_string = '"single\\backslash"'
        expected_output = '"single\\\\backslash"'
        fixed_output = _format_quotes(input_string)
        self.assertEqual(fixed_output, expected_output)
        assert json.loads(fixed_output)

    def test_double_backslash(self):
        input_string = '"double\\\\backslash"'
        expected_output = '"double\\\\backslash"'
        fixed_output = _format_quotes(input_string)
        self.assertEqual(fixed_output, expected_output)
        assert json.loads(fixed_output)

    def test_triple_backslash(self):
        input_string = '"triple\\\\\\backslash"'
        expected_output = '"triple\\\\\\\\backslash"'
        fixed_output = _format_quotes(input_string)
        self.assertEqual(fixed_output, expected_output)
        assert json.loads(fixed_output)

    def test_mixed_backslashes(self):
        input_string = '["mixed\\", "backslashes\\\\", "here\\\\\\"]'
        expected_output = '["mixed\\\\", "backslashes\\\\", "here\\\\\\\\"]'
        fixed_output = _format_quotes(input_string)
        self.assertEqual(fixed_output, expected_output)
        assert json.loads(fixed_output)

    def test_no_backslashes(self):
        input_string = '"no backslashes here"'
        expected_output = '"no backslashes here"'
        fixed_output = _format_quotes(input_string)
        self.assertEqual(fixed_output, expected_output)
        assert json.loads(fixed_output)
