import logging
import re
from orderedset import OrderedSet
from ..lexer import Token
import weakref

#parse tree
class Node(object):
    def __init__(self, value, children=[]):
        self.value = value
        self.children = OrderedSet(children)
        self._parent = None

    @property
    def parent(self):
        if self._parent is None:
            return None
        else:
            return self._parent()

    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = None
        else:
            self._parent = weakref.ref(value)

    def __repr__(self):
        return "<Node name: '%r' children: '%r'>" % (self.value.name, self.children)

class ObjectNode(Node):
    def __init__(self, value, children=[]):
        super(ObjectNode, self).__init__(value, children)

    def has_object(self):
        return hasattr(self, "object")

class AbstractTreeBuilder(object):
    def __init__(self, root_value):
        self.root = Node(root_value)
        self.current_node = self.root

    def up(self, success = True):
        pass

    def down(self, value):
        pass

    def delete(self):
        pass

    def build(self):
        pass

class TreeBuilderSupport(AbstractTreeBuilder):
    def __init__(self, root_value, node_class=Node):
        self.node_class = node_class
        self.root = node_class(root_value)
        self.current_node = self.root

    def up(self, success = True):
        assert(self.current_node.parent != None)
        self.current_node = self.current_node.parent

    def down(self, value):
        new_child = Node(value)

        self.current_node.children.add(new_child)
        new_child.parent = self.current_node
        self.current_node = new_child  

    def delete(self):
        node_to_delete = self.current_node
        self.up(False)
        self.current_node.children.remove(node_to_delete)
        node_to_delete.children.clear()

    def build(self):
        tree = Tree(self.root)
        self.root = None
        return tree

class TreeBuilder(TreeBuilderSupport):
    def __init__(self, root_value):
        super(TreeBuilder, self).__init__(root_value)

class AbstractObjectTreeBuilder(TreeBuilderSupport):
    def __init__(self, root_value):
        super(AbstractObjectTreeBuilder, self).__init__(root_value, node_class=ObjectNode)
        self.builders = self._find_builders()
        self.level = 0

    def up(self, success = True):
        self.level = self.level - 1
        last_node = self.current_node

        super(AbstractObjectTreeBuilder, self).up()

        if success:
            if last_node.value.name in self.builders:
                last_node.object = self._build_object(last_node)

    def down(self, success = True):
        self.level = self.level + 1
        super(AbstractObjectTreeBuilder, self).down(success)

    def build(self):
        self.root.object = self._build_object(self.root)

        tree = super(AbstractObjectTreeBuilder, self).build()

        return tree

    def _find_builders(self):
        attributes = ((attribute_name, getattr(self, attribute_name)) for attribute_name in dir(self))
        builders = {}

        for name, attribute in attributes:
            if name.startswith("build_"):
                builder_for_object = name.replace("build_", "", 1)
                builders[builder_for_object] = attribute

        return builders

    def _build_object(self, node):
        builder = self.builders.get(node.value.name, None)

        if builder != None:
            build_object = builder(node)
            node.children.clear() #delete children, they are no longer needed
            return build_object
        else:
            raise KeyError("no builder for %s found" % node.value.name)       

class Tree(object):
    def __init__(self, root):
        self.root = root

    def to_dot(self):
        max_recursion = 100
        def recursive_to_dot(node, level):
            if level > max_recursion:
                return ""
            dot = ""
            label = node.value.name
            if isinstance(node.value, Token):
                label += " <%s>" % node.value.match.group()
            name = "ID" + str(id(node))

            dot += "%s [label=\"%s\"]\n" % (name, re.escape(label))

            for child in node.children:
                dot += "\n" + recursive_to_dot(child, level + 1)

            for child in node.children:
                child_name = "ID" + str(id(child))
                dot += "%s -> %s;\n" % (name, child_name)

            return dot

        dot_header = "digraph graphname {\n"
        dot_footer = "\n}"

        return dot_header + recursive_to_dot(self.root, 0) + dot_footer

    def write_to_dot(self, fname):
        f = open(fname, "w")
        f.write(self.to_dot())
        f.close()

    def __repr__(self):
        return str(self.root)