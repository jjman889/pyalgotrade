# PyAlgoTrade
#
# Copyright 2011-2013 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

from pyalgotrade.utils import collections

import unittest
import datetime


class CollectionsTestCase(unittest.TestCase):
    def testEmptyIntersection(self):
        values, ix1, ix2 = collections.intersect([1, 2, 3], [4, 5, 6])
        self.assertEqual(len(values), 0)
        self.assertEqual(len(ix1), 0)
        self.assertEqual(len(ix2), 0)

        values, ix1, ix2 = collections.intersect([], [])
        self.assertEqual(len(values), 0)
        self.assertEqual(len(ix1), 0)
        self.assertEqual(len(ix2), 0)

    def testFullIntersection(self):
        values, ix1, ix2 = collections.intersect([1, 2, 3], [1, 2, 3])
        self.assertEqual(len(values), 3)
        self.assertEqual(len(ix1), 3)
        self.assertEqual(len(ix2), 3)
        self.assertEqual(ix1, ix2)

    def testPartialIntersection1(self):
        values, ix1, ix2 = collections.intersect([0, 2, 4], [1, 2, 3])
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], 2)
        self.assertEqual(ix1[0], 1)
        self.assertEqual(ix2[0], 1)

    def testPartialIntersection2(self):
        values, ix1, ix2 = collections.intersect([1, 2, 4], [1, 2, 3])
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0], 1)
        self.assertEqual(values[1], 2)
        self.assertEqual(ix1[0], 0)
        self.assertEqual(ix1[1], 1)
        self.assertEqual(ix2[0], 0)
        self.assertEqual(ix2[1], 1)

    def testPartialIntersection3(self):
        values, ix1, ix2 = collections.intersect([1, 2, 5], [1, 3, 5])
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0], 1)
        self.assertEqual(values[1], 5)
        self.assertEqual(ix1[0], 0)
        self.assertEqual(ix1[1], 2)
        self.assertEqual(ix2[0], 0)
        self.assertEqual(ix2[1], 2)

    def testPartialIntersection4(self):
        values, ix1, ix2 = collections.intersect([1, 2, 3], [2, 4, 6])
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], 2)
        self.assertEqual(ix1[0], 1)
        self.assertEqual(ix2[0], 0)

    def testPartialIntersection5(self):
        values, ix1, ix2 = collections.intersect([1, 2, 3], [3, 6])
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], 3)
        self.assertEqual(ix1[0], 2)
        self.assertEqual(ix2[0], 0)

    def testPartialIntersection6(self):
        v1 = [1, 1, 2, 2, 3, 3]
        v2 = [1, 2, 3]

        values, ix1, ix2 = collections.intersect(v1, v2)
        self.assertEqual(values, [1, 2, 3])
        self.assertEqual(ix1, [0, 2, 4])
        self.assertEqual(ix2, [0, 1, 2])

        values, ix2, ix1 = collections.intersect(v2, v1)
        self.assertEqual(values, [1, 2, 3])
        self.assertEqual(ix1, [0, 2, 4])
        self.assertEqual(ix2, [0, 1, 2])

    def testPartialIntersectionIncludeNones(self):
        v1 = [None, 1, None, None, 2, None, 3, None, 4]
        v2 = [1, None, 2, None, 3, 4]

        values, ix1, ix2 = collections.intersect(v1, v2)
        self.assertEqual(values, [1, None, 2, None, 3, 4])
        self.assertEqual(ix1, [1, 2, 4, 5, 6, 8])
        self.assertEqual(ix2, [0, 1, 2, 3, 4, 5])

        values, ix2, ix1 = collections.intersect(v2, v1)
        self.assertEqual(values, [1, None, 2, None, 3, 4])
        self.assertEqual(ix1, [1, 2, 4, 5, 6, 8])
        self.assertEqual(ix2, [0, 1, 2, 3, 4, 5])

    def testPartialIntersectionSkipNones(self):
        v1 = [None, 1, None, None, 2, None, 3, None, 4]
        v2 = [1, None, 2, None, 3, 4]

        values, ix1, ix2 = collections.intersect(v1, v2, True)
        self.assertEqual(values, [1, 2, 3, 4])
        self.assertEqual(ix1, [1, 4, 6, 8])
        self.assertEqual(ix2, [0, 2, 4, 5])

        values, ix2, ix1 = collections.intersect(v2, v1, True)
        self.assertEqual(values, [1, 2, 3, 4])
        self.assertEqual(ix1, [1, 4, 6, 8])
        self.assertEqual(ix2, [0, 2, 4, 5])

    def testFullIntersectionWithDateTimes(self):
        size = 1000
        dateTimes1 = []
        dateTimes2 = []
        now = datetime.datetime.now()
        for i in xrange(size):
            dateTimes1.append(now + datetime.timedelta(seconds=i))
            dateTimes2.append(now + datetime.timedelta(seconds=i))

        self.assertEqual(dateTimes1, dateTimes2)

        values, ix1, ix2 = collections.intersect(dateTimes1, dateTimes2)
        self.assertEqual(values, dateTimes1)
        self.assertEqual(values, dateTimes2)
        self.assertEqual(ix1, range(size))
        self.assertEqual(ix1, ix2)

    def testNumPyDeque(self):
        d = collections.NumPyDeque(10)
        self.assertEqual(len(d), 0)

        for i in range(10):
            d.append(i)
        self.assertEqual(d[0], 0)
        self.assertEqual(d[9], 9)
        self.assertEqual(d[-1], 9)
        self.assertEqual(d[-2], 8)
        self.assertEqual(d[0:3].sum(), 3)

        for i in range(3):
            d.append(i)
        self.assertEqual(len(d), 10)
        self.assertEqual(d[0], 3)
        self.assertEqual(d[9], 2)
        self.assertEqual(d[-1], 2)
        self.assertEqual(d[-2], 1)

    def testNumPyDequeResize(self):
        d = collections.NumPyDeque(10)

        self.assertEqual(len(d), 0)
        for i in range(20):
            d.append(i)
        self.assertEqual(d[0], 10)
        self.assertEqual(d[9], 19)
        self.assertEqual(d[-1], 19)
        self.assertEqual(len(d), 10)

        d.resize(5)
        self.assertEqual(len(d), 5)
        self.assertEqual(d[-0], 10)
        self.assertEqual(d[4], 14)
        self.assertEqual(d[-1], 14)

        d.resize(10)
        self.assertEqual(len(d), 5)
        self.assertEqual(d[-0], 10)
        self.assertEqual(d[4], 14)
        self.assertEqual(d[-1], 14)

        d.append(15)
        self.assertEqual(len(d), 6)
        self.assertEqual(d[5], 15)
        self.assertEqual(d[-1], 15)
