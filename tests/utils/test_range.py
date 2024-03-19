from unittest import TestCase
from src.pyil2.utils.range import LimitedRange

class LimitedRangeTest(TestCase):
    def test_from_string(self):
        range = LimitedRange.resolve('[100-200]')
        self.assertEqual(range.start, 100)
        self.assertEqual(range.end, 200)
        self.assertEqual(range.count, 101)
        self.assertEqual(str(range), '[100-200]')

        range2 = LimitedRange.resolve('[100]')
        self.assertEqual(range2.start, 100)
        self.assertEqual(range2.end, 100)
        self.assertEqual(str(range2), '[100]')
    
    def test_equal(self):
        range = LimitedRange(start=100, end=200)
        range2 = LimitedRange(start=100, count=101)
        self.assertTrue(range == range2)
    
    def test_in(self):
        range = LimitedRange(start=100, end=200)
        self.assertTrue(range in range)
        self.assertTrue(150 in range)
        
        range2 = LimitedRange(start=100, end=150)
        self.assertTrue(range2 in range)

        range3 = LimitedRange(start=50, end=150)
        self.assertFalse(range3 in range)
    
        range4 = LimitedRange(start=150, end=250)
        self.assertFalse(range4 in range)

        range5 = LimitedRange(start=50, end=250)
        self.assertFalse(range5 in range)
        
        range6 = LimitedRange(start=50, end=70)
        self.assertFalse(range6 in range)
        
        range7 = LimitedRange(start=210, end=250)
        self.assertFalse(range7 in range)
        

    def test_overlaps(self):
        range = LimitedRange(start=100, end=200)
        self.assertTrue(range.overlaps_with(range))
        
        range2 = LimitedRange(start=100, end=150)
        self.assertTrue(range.overlaps_with(range2))

        range3 = LimitedRange(start=50, end=150)
        self.assertTrue(range.overlaps_with(range3))
    
        range4 = LimitedRange(start=150, end=250)
        self.assertTrue(range.overlaps_with(range4))

        range5 = LimitedRange(start=50, end=250)
        self.assertTrue(range.overlaps_with(range5))

        range6 = LimitedRange(start=50, end=70)
        self.assertFalse(range.overlaps_with(range6))
        
        range7 = LimitedRange(start=210, end=250)
        self.assertFalse(range.overlaps_with(range7))
        
        
    