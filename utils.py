from .Scalar import Scalar

def getInput(inputShape):
    if len(inputShape)==0:
        return Scalar()
    else:
        return [getInput(inputShape[1:]) for _ in range (inputShape[0])]

def getOutputShape(output):
    shape = []
    subarr = output
    while isinstance(subarr, list):
        shape.append(len(subarr))
        subarr = subarr[0]
    return shape

def setAsOutput(output):
    if isinstance(output, list):
        return [setAsOutput(element) for element in output]
    else:
        return Scalar(output).asOutput()
