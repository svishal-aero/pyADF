class FunctionNode:

    def __init__(self, functionName, idList):
        self.functionName = functionName
        self.idList = idList

    def isIdenticalto(self, other):
        if self.functionName==other.functionName:
            if self.idList==other.idList:
                return True
        return False

    def forwardStatement(self, id):
        string = self.functionName + '(___phi, ' + id
        for id in self.idList:
            string += ', ' + str(self.idList[id])
        string += ')'
        return string

    def reverseStatement(self, id):
        string = self.functionName + '(___psi, ' + id
        for id in self.idList:
            string += ', ' + str(self.idList[id])
        string += ')'
        return string
