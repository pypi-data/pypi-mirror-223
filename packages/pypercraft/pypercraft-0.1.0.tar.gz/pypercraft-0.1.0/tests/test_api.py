"""
Test for API
"""
import os
import unittest
from fastapi.testclient import TestClient
from api.api import app


class TestGenerateDocumentAPI(unittest.TestCase):
    """
    Class that tests the api
    """

    def setUp(self):
        self.client = TestClient(app)

    def test_generate_document_valid_input(self):
        """
        Test core functionality of api
        """
        response = self.client.get("/generate_document/",
                                   params={
                                       "query": "Test query",
                                       "topic": "Test topic",
                                       "num_pages": 5,
                                       "tone": "Formal",
                                       "api_key": os.getenv("OPENAI_API_KEY")
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("intro", response.json())
        self.assertIn("body", response.json())
        self.assertIn("conclusion", response.json())

    def test_generate_document_invalid_query(self):
        """
        Test when missing query
        """
        response = self.client.get("/generate_document/",
                                   params={
                                       "topic": "Test topic",
                                       "num_pages": 5,
                                       "tone": "Formal",
                                       "api_key": os.getenv("OPENAI_API_KEY")
                                   })
        self.assertNotEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
