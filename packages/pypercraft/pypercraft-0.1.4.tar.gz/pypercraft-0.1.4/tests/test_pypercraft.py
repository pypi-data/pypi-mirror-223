"""
Test class for Pypercraft
"""

import os
import unittest
import datetime
from pypercraft.pypercraft import Pypercraft


def get_current_datetime():
    """
    Gets current time
    """
    current_datetime = datetime.datetime.now()
    return current_datetime


class TestPypercraft(unittest.TestCase):
    """
    Tests the Pypercraft Class
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up the class instance
        """
        cls.api_key = os.getenv("OPENAI_API_KEY")
        cls.query = """An article about deep learning applications on space
        ships in star wars movie series"""
        cls.topic = "Deep Learning and Star Wars"
        cls.num_pages = 2
        cls.tone = "professional"
        cls.pypercraft = Pypercraft(cls.query, cls.topic, cls.num_pages, cls.tone, cls.api_key)

    def test_check_inputs(self):
        """
        Tests the inputs to the model
        """
        self.assertEqual(self.tone, "professional")
        self.assertEqual(self.query, """An article about deep learning applications on
        space ships in star wars movie series""")
        self.assertEqual(self.topic, "Deep Learning and Star Wars")
        self.assertEqual(self.num_pages, 2)

    def test_generate_title(self):
        """
        Tests the title
        """
        title = self.pypercraft.generate_title()
        self.assertIsInstance(title, str)
        self.assertNotEqual(title, "")
        self.assertGreater(len(title), 10)

    def test_generate_introduction(self):
        """
        Tests the introduction
        """
        introduction = self.pypercraft.generate_introduction()
        self.assertIsInstance(introduction, str)
        self.assertNotEqual(introduction, "")
        self.assertGreater(len(introduction), 10)

    def test_generate_body(self):
        """
        Tests the body
        """
        body = self.pypercraft.generate_body()
        self.assertIsInstance(body, str)
        self.assertNotEqual(body, "")
        self.assertGreater(len(body), 10)

    def test_generate_conclusion(self):
        """
        Tests the conclusion
        """
        conclusion = self.pypercraft.generate_conclusion()
        self.assertIsInstance(conclusion, str)
        self.assertNotEqual(conclusion, "")
        self.assertGreater(len(conclusion), 10)

    def test_construct(self):
        """
        Tests the construction method
        """
        paper = self.pypercraft.construct()

        self.assertIsInstance(paper, dict)
        self.assertIn("title", paper)
        self.assertIn("introduction", paper)
        self.assertIn("body", paper)
        self.assertIn("conclusion", paper)
        self.assertNotEqual(paper["title"], "")
        self.assertNotEqual(paper["introduction"], "")
        self.assertNotEqual(paper["body"], "")
        self.assertNotEqual(paper["conclusion"], "")
        self.assertGreater(len(paper["title"]), 10)
        self.assertGreater(len(paper["introduction"]), 10)
        self.assertGreater(len(paper["body"]), 10)
        self.assertGreater(len(paper["conclusion"]), 10)

    def test_construct_export(self):
        """
        Tests the export method
        """
        paper = self.pypercraft.construct()

        self.assertIsInstance(paper, dict)
        self.assertIn("title", paper)
        self.assertIn("introduction", paper)
        self.assertIn("body", paper)
        self.assertIn("conclusion", paper)
        self.assertNotEqual(paper["title"], "")
        self.assertNotEqual(paper["introduction"], "")
        self.assertNotEqual(paper["body"], "")
        self.assertNotEqual(paper["conclusion"], "")
        self.assertGreater(len(paper["title"]), 10)
        self.assertGreater(len(paper["introduction"]), 10)
        self.assertGreater(len(paper["body"]), 10)
        self.assertGreater(len(paper["conclusion"]), 10)
        self.pypercraft.export_docx(f"tmp/test_file_{get_current_datetime()}.docx")


if __name__ == "__main__":
    unittest.main()
