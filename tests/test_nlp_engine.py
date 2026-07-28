import unittest
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from preprocess import preprocess_text
from synonym_mapper import map_synonyms
from spell_corrector import correct_spelling
from scoring_engine import recommend_best_career, find_mentioned_career
from recommendation import recommend_career
from intent_router import detect_followup


class TestNLPEngine(unittest.TestCase):

    def test_preprocess_text(self):
        text = "I love Machine Learning and Python!"
        processed = preprocess_text(text)
        self.assertIn("machine", processed)

    def test_synonym_mapping(self):
        self.assertIn("power bi", map_synonyms("I use PBI"))
        self.assertIn("user interface", map_synonyms("I design UI UX"))
        self.assertIn("search engine optimization", map_synonyms("I work in SEO"))

    def test_tech_career_recommendation(self):
        res = recommend_career("I love machine learning and python")
        self.assertIsInstance(res, dict)
        self.assertIn("Engineer", res["career"])

    def test_arts_career_recommendation(self):
        res = recommend_career("I enjoy Figma wireframing and user interface design")
        self.assertIsInstance(res, dict)
        self.assertEqual(res["career"], "UI/UX Designer")

    def test_commerce_career_recommendation(self):
        res = recommend_career("I want to work in digital marketing and SEO")
        self.assertIsInstance(res, dict)
        self.assertEqual(res["career"], "Digital Marketer")

        res_ba = recommend_career("I like requirements gathering and agile user stories")
        self.assertIsInstance(res_ba, dict)
        self.assertEqual(res_ba["career"], "Business Analyst")

        res_fa = recommend_career("I enjoy financial modeling and DCF valuation")
        self.assertIsInstance(res_fa, dict)
        self.assertEqual(res_fa["career"], "Financial Analyst")

    def test_followup_intent_detection(self):
        self.assertEqual(detect_followup("what is the roadmap"), "roadmap")
        self.assertEqual(detect_followup("how much salary can I get"), "salary")
        self.assertEqual(detect_followup("what skills are required"), "skills")

    def test_dynamic_followup_career_extraction(self):
        res = recommend_career("need ai web development roadmap")
        self.assertIsInstance(res, str)
        self.assertIn("Full Stack Developer", res)
        self.assertIn("HTML", res)


if __name__ == "__main__":
    unittest.main()
