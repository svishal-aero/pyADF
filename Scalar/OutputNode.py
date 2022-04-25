class OutputNode:

    def __init__(self, refId): self.refId = refId

    def isIdenticalTo(self, node): return False

    def forwardStatement(self, id): return 'EQUAL(%d, %d)' % (id, self.refId)

    def reverseStatement(self, id): return 'D_EQUAL(%d, %d)' % (id, self.refId)
