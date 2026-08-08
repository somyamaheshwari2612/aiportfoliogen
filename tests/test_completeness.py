"""
Unit tests for completeness scoring module (analysis/completeness.py).
"""

import unittest
from analysis.completeness import calculate_completeness


class TestCompletenessModule(unittest.TestCase):

    def test_type_error_on_non_dict(self):
        with self.assertRaises(TypeError):
            calculate_completeness("invalid_string_input")
        with self.assertRaises(TypeError):
            calculate_completeness([1, 2, 3])

    def test_value_error_on_empty_dict(self):
        with self.assertRaises(ValueError):
            calculate_completeness({})

    def test_full_portfolio_score(self):
        data = {
            "personal_info": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "555-1234",
                "headline": "Lead AI Engineer",
                "location": "New York, NY"
            },
            "summary": "Experienced AI Engineer specializing in LLMs, Flask, and scalable cloud systems.",
            "experience": [
                {
                    "title": "Senior AI Engineer",
                    "company": "Tech Corp",
                    "description": "Led AI development."
                },
                {
                    "title": "Software Developer",
                    "company": "Dev Solutions",
                    "description": "Built REST APIs."
                }
            ],
            "education": [
                {
                    "degree": "B.S. Computer Science",
                    "institution": "Stanford University"
                }
            ],
            "skills": ["Python", "Flask", "PyTorch", "Docker", "Git"],
            "projects": [
                {"title": "Portfolio Generator"},
                {"title": "Weather Dashboard"}
            ],
            "social_links": {
                "linkedin": "https://linkedin.com/in/janedoe",
                "github": "https://github.com/janedoe",
                "website": "https://janedoe.dev"
            }
        }
        score = calculate_completeness(data)
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 85)
        self.assertLessEqual(score, 100)

    def test_deduplication_and_caps(self):
        # 20 duplicate experience items should NOT inflate the score past section cap
        duplicate_experience = [
            {"title": "Software Engineer", "company": "Company A"}
        ] * 20

        data = {
            "personal_info": {"name": "John Doe", "email": "john@example.com"},
            "experience": duplicate_experience,
            "skills": ["Python", "Python", "PYTHON", "python"]
        }
        score = calculate_completeness(data)
        self.assertLessEqual(score, 100)
        # Unique skills should count as 1 skill (3 pts), experience as 1 job (10 pts), personal info (10 pts)
        self.assertGreater(score, 0)

    def test_bonus_points_social_links(self):
        base_data = {
            "personal_info": {"name": "Jane", "email": "jane@test.com"},
            "skills": ["Python", "Flask"]
        }
        score_without_bonus = calculate_completeness(base_data)

        base_data_with_bonus = dict(base_data)
        base_data_with_bonus["social_links"] = {
            "github": "https://github.com/jane",
            "linkedin": "https://linkedin.com/in/jane"
        }
        score_with_bonus = calculate_completeness(base_data_with_bonus)

        self.assertGreater(score_with_bonus, score_without_bonus)

    def test_malformed_data_fail_safe(self):
        # Malformed entries inside lists (e.g. integer inside experience list) should not crash
        malformed_data = {
            "personal_info": "Not a dict",
            "experience": [123, None, "bad_entry"],
            "education": "Not a list",
            "skills": 456
        }
        score = calculate_completeness(malformed_data)
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)


if __name__ == "__main__":
    unittest.main()
