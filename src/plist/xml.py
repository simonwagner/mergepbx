from __future__ import absolute_import

from xml.dom.minidom import parse as parseXML
import xml.dom
from itertools import islice, izip, tee
from collections import OrderedDict

ENCODING_ALIASES = {
    "UTF-8":"UTF8",
}

class XMLPlistReader(object):
    def __init__(self, f, name=None):
        self._f = f
        self.name = name
        self._encoding = None

        self._elementVisitors = {
            u"array" : self._visitArray,
            u"dict" : self._visitDict,
            u"key" : self._visitKey,
            u"string" : self._visitString,
        }

    def read(self):
        #parse file
        dom = parseXML(self._f)
        self._encoding = dom.encoding

        if not dom.doctype.publicId == u"-//Apple//DTD PLIST 1.0//EN":
            raise ValueError("The given file is no XML plist file")

        #get root
        root = dom.documentElement
        mainObjectElement = _childElements(root)[0]

        return self._visitElement(mainObjectElement)

    def _visitElement(self, element):
        tag = element.nodeName
        if tag in self._elementVisitors:
            visitor = self._elementVisitors[tag]
            return visitor(element)
        else:
            raise Exception("unknown element '%s' in XML plist" % tag)

    def _visitArray(self, element):
        value = []
        for child in _childElements(element):
            childValue = self._visitElement(child)
            value.append(childValue)
        return value

    def _visitDict(self, element):
        childIter = _iterChildElements(element)
        items = [(self._visitElement(keyNode), self._visitElement(valueNode)) for (keyNode, valueNode) in _itemsFromIterable(childIter)]
        keys = [key for (key, value) in items]
        values = [value for (key, value) in items]
        return OrderedDict(zip(keys, values))

    def _visitKey(self, element):
        return _nodeText(element)

    def _visitString(self, element):
        return _nodeText(element)

    def get_encoding(self):
        encoding = ENCODING_ALIASES.get(self._encoding, self._encoding)
        return encoding

    def close(self):
        self.f.close()

def _iterChildrenWithType(node, type):
    for childNode in node.childNodes:
        if childNode.nodeType == type:
            yield childNode

def _iterChildElements(node):
    return _iterChildrenWithType(node, xml.dom.Node.ELEMENT_NODE)

def _childElements(node):
    return list(_iterChildElements(node))

def _nodeText(node):
    inodes = _iterChildrenWithType(node, xml.dom.Node.TEXT_NODE)
    return unicode.join(u"", (inode.data for inode in inodes))

def _itemsFromIterable(iter):
    iters = tee(iter, 2)
    ikeys = islice(iters[0], None, None, 2)
    ivalues = islice(iters[1], 1, None, 2)

    return izip(ikeys, ivalues)

#TODO: create XMLPlistWriter
