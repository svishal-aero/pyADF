from ..CodeGeneration.FormattedBuffer import FormattedBuffer
from .ConditionalHandler import ConditionalHandler

class Graph:

    def __init__(self):
        self.nodeList           = []
        self.conditionalHandler = ConditionalHandler()
        self.forwardBuffer      = FormattedBuffer()
        self.reverseBuffer      = FormattedBuffer(openTag='}',closeTag='{')
        self.includes           = []

    @property
    def tapeSize(self): return len(self.nodeList)

    def initCompilationPass(self):
        self.conditionalHandler.initCompilationPass()

    def finalizeCompilationPass(self, disableDerivs=False):
        self.forwardBuffer.write('getOutputs(self, %d);' % (self.tapeSize))
        if not disableDerivs:
            self.forwardBuffer.write('updateDerivs(self, %d);' % (self.tapeSize))
        self.conditionalHandler.finalizeCompilationPass()
