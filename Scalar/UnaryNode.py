class UnaryNode:

    def __init__(self, operator, xid):
        self.operator = operator
        self.xid = xid
    
    def isIdenticalTo(self, node):
        return self.operator==node.operator and self.xid==node.xid
    
    def forwardStatement(self, id):
        return '%s(%d, %d)' % (self.operator, id, self.xid)
    
    def reverseStatement(self, id):
        return 'D_%s(%d, %d)' % (self.operator, id, self.xid)
