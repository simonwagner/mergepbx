import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

from pbxproj.core import DictionaryBoundObject

class DictionaryBoundObjectTest(unittest.TestCase):
    def test_readValue(self):
        data = {"a": "hello", "b" : "world"}
        boundObj = DictionaryBoundObject(data)

        self.assertEquals("hello", boundObj.a)
        self.assertEquals("world", boundObj.b)

    def test_writeValue(self):
        data = {"a": "hello", "b" : "world"}
        boundObj = DictionaryBoundObject(data)

        boundObj.b = "simon"
        self.assertEquals("simon", boundObj.b)
        self.assertEquals("simon", data["b"])
