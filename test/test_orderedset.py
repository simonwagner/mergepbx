from orderedset import OrderedSet

import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

class TokenStreamTest(unittest.TestCase):
    def test_clear(self):
        s = OrderedSet((1,2,3,4))
        s.clear()

    def test_weakref(self):
        s = OrderedSet((1,2,3,4))
        actual = list(s)

        self.assertEqual(actual , [1,2,3,4])

if __name__ == '__main__':
    unittest.main()
