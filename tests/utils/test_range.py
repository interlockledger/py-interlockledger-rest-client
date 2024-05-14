# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
