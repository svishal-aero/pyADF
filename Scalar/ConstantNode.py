class ConstantNode:

    def __init__(self, value):      self.value = value

    def isIdenticalTo(self, node):  return self.value==node.value

    def forwardStatement(self, id): return 'CONST(%d, %.10le)' % (id, self.value)

    def reverseStatement(self, id): return None
