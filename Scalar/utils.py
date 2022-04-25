__nodeDoesNotExistInGraph = -1

def __indexAtWhichNodeAlreadyExists(newNode, graph):
    id = __nodeDoesNotExistInGraph
    for i, graphNode in enumerate(graph.nodeList):
        if type(newNode) is type(graphNode):
            if newNode.isIdenticalTo(graphNode):
                id = i
    return id

def getIndexInGraph(newNode, graph):
    id = __indexAtWhichNodeAlreadyExists(newNode, graph)
    if id==__nodeDoesNotExistInGraph:
        id = len(graph.nodeList)
        graph.nodeList.append(newNode)
        graph.forwardBuffer.write(newNode.forwardStatement(id), newNode.forwardStatement(id) is not None)
        graph.reverseBuffer.write(newNode.reverseStatement(id), newNode.reverseStatement(id) is not None)
    return id
