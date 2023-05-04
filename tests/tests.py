import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payout import calculate_payouts


class TestPayouts(unittest.TestCase):
    def test_calculate_payouts(self):
        # Test 1
        prize_pool, payouts = calculate_payouts(10, 20, 100, 4)
        self.assertEqual(prize_pool, 300)
        self.assertEqual(payouts, {1: 150, 2: 90, 3: 40, 4: 20})
        self.assertEqual(sum(payouts.values()), prize_pool)

        # Test 2
        prize_pool, payouts = calculate_payouts(20, 5, 0, 4)
        self.assertEqual(prize_pool, 100)
        self.assertEqual(payouts, {1: 50, 2: 30, 3: 15, 4: 5})
        self.assertEqual(sum(payouts.values()), prize_pool)

        # Test 3
        prize_pool, payouts = calculate_payouts(4, 5, 100, 4)
        self.assertEqual(prize_pool, 120)
        self.assertEqual(payouts, {1: 60, 2: 35, 3: 20, 4: 5})
        self.assertEqual(sum(payouts.values()), prize_pool)

        # Test 4
        with self.assertRaises(ValueError):
            calculate_payouts(-10, 0, 0, 4)
        with self.assertRaises(ValueError):
            calculate_payouts(10, -20, 0, 4)
        with self.assertRaises(ValueError):
            calculate_payouts(10, 20, -100, 4)
        with self.assertRaises(ValueError):
            calculate_payouts(10, 20, 100, 1)
        with self.assertRaises(ValueError):
            calculate_payouts(4, 5, 100, 5)


if __name__ == "__main__":
    unittest.main()
