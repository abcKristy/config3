import unittest
from config_parser import ConfigParser

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser()

    def test_constants(self):
        text = "const1 = 10; const2 = \"value\";"
        self.parser._process_constants(text)
        self.assertEqual(self.parser.constants["const1"], 10)
        self.assertEqual(self.parser.constants["const2"], "value")

    def test_constant_replacement(self):
        text = "const1 = 10; text $const1$;"
        self.parser._process_constants(text)
        result = self.parser._replace_constants(text)
        self.assertIn("text 10;", result)

    def test_remove_comments(self):
        text = "text {# this is a comment #} more text"
        result = self.parser._remove_comments(text)
        self.assertEqual(result.strip(), "text  more text")

    def test_structure(self):
        text = """
        begin
        key1 := 10;
        key2 := "value";
        end
        """
        result = self.parser._process_structure(text)
        self.assertEqual(result, [{"key1": 10, "key2": "value"}])

if __name__ == "main":
    unittest.main()