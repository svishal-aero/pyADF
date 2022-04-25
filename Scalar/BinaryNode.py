class BinaryNode:

    def __init__(self, operator, xid, yid):
        self.operator = operator
        self.xid = xid
        self.yid = yid
    
    def isIdenticalTo(self, other):
        if self.__hasSameOperatorAs(other):
            if self.__hasSameOperandsAs(other):
                return True
            if self.__hasSameOperandsButFlippedAs(other) and self.__isCommutative:
                return True
        return False
    
    def forwardStatement(self, id):
        return '%s(%d, %d, %d)' % (self.operator, id, self.xid, self.yid)
    
    def reverseStatement(self, id):
        return 'D_%s(%d, %d, %d)' % (self.operator, id, self.xid, self.yid)

    @property
    def __isCommutative(self):
        return self.operator in ['ADD', 'MUL', 'FMAX', 'FMIN']

    def __hasSameOperatorAs(self, other):
        return self.operator == other.operator

    def __hasSameOperandsAs(self, other):
        return self.xid == other.xid and self.yid == other.yid

    def __hasSameOperandsButFlippedAs(self, other):
        return self.xid == other.yid and self.yid == other.xid
