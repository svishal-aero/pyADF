from .GraphEntity import GraphEntity

class ConditionalSwitch(GraphEntity):

    def __init__(self, operator, xid, yid):
        self.operator = operator
        self.xid = xid
        self.yid = yid
        self.value = None
        self.position = len(self.graph.nodeList)
        self.initializeTrueBranch()

    @property
    def inverseOperator(self):
        inverseDict = { '==':'!=', '<':'>=', '>':'<=',
                        '!=':'==', '>=':'<', '<=':'>', }
        return inverseDict[self.operator]

    def __purgeFollowingOperationsInGraph(self):
        del self.graph.nodeList[self.position:]

    def initializeTrueBranch(self):
        self.value = True
        x = '___phi[%d]' % (self.xid)
        y = '___phi[%d]' % (self.yid)
        expr = x + self.operator + y
        self.forward.write('if('+expr+')')
        self.forward.openScope()
        self.reverse.openScope()

    def switchToFalseBranch(self):
        self.value = False
        self.__purgeFollowingOperationsInGraph()
        self.forward.closeScope()
        self.forward.write('else')
        self.forward.openScope()
        self.reverse.closeScope()
        self.reverse.write('else')
        self.reverse.openScope()

    def finalizeFalseBranch(self):
        x = '___phi[%d]' % (self.xid)
        y = '___phi[%d]' % (self.yid)
        expr = x + self.inverseOperator + y
        self.__purgeFollowingOperationsInGraph()
        self.forward.closeScope()
        self.reverse.closeScope()
        self.reverse.write('if('+expr+')')
