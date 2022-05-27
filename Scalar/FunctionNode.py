class FunctionNode:

    def __init__(self, functionName, idList):
        self.functionName = functionName
        self.idList = idList

    def isIdenticalTo(self, other):
        if self.functionName==other.functionName:
            if self.idList==other.idList:
                return True
        return False

    def forwardStatement(self, id):
        string = '___phi[' + str(id) + '] = ' + self.functionName
        string += '.calculate(___phi+' + str(self.idList[0])
        for i in range(1,len(self.idList)):
            string += ', ___phi+' + str(self.idList[i])
        string += ');'
        return string

    def reverseStatement(self, id):
        string = self.functionName + '.d_calculate('
        string += '___psi+' + str(id)
        for i in range(len(self.idList)):
            string += ', ___psi+' + str(self.idList[i])
        string += ');'
        return string
