class ConditionalHandler:

    def __init__(self):
        self.nProcessedConditionals = 0
        self.knownConditionals = []

    def initCompilationPass(self): self.nProcessedConditionals = 0

    def finalizeCompilationPass(self): self.__modifyControlFlowForNextPass()

    @property
    def nKnownConditionals(self): return len(self.knownConditionals)

    @property
    def lastKnownConditional(self): return self.knownConditionals[-1]

    def __removeLastKnownConditional(self): del self.knownConditionals[-1]

    def __modifyControlFlowForNextPass(self):
        while self.nKnownConditionals > 0:
            if self.lastKnownConditional.value==False:
                self.lastKnownConditional.finalizeFalseBranch()
                self.__removeLastKnownConditional()
            else:
                self.lastKnownConditional.switchToFalseBranch()
                break
