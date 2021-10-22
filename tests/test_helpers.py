import unittest
from datetime import date
from app.budget import helpers as budget_h


class TestDataMethodsTestCase(unittest.TestCase):
    def test_month_days(self):
        self.assertEqual(
            budget_h.get_month_days(month=1, year=2020)[0], date(2020, 1, 1)
        )
        self.assertEqual(
            budget_h.get_month_days(month=1, year=2020)[1], date(2020, 1, 31)
        )
        self.assertNotEqual(
            budget_h.get_month_days(month=1, year=2020)[1], date(2020, 1, 30)
        )
        self.assertEqual(
            budget_h.get_month_days(month=None, year=None), budget_h.get_month_days()
        )
        self.assertRaises(ValueError, budget_h.get_month_days, -1)
        self.assertRaises(ValueError, budget_h.get_month_days, 13)
        self.assertRaises(TypeError, budget_h.get_month_days, "1")
