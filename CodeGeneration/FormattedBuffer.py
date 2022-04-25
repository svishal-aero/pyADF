class FormattedBuffer:
    
    def __init__(self, openTag='{', closeTag='}', tab='\t'):
        self.lines     = []
        self.indent   = ''
        self.tab      = tab
        self.openTag  = openTag
        self.closeTag = closeTag
        self.active   = True

    def write(self, text, flag=True):
        if self.active and flag:
            self.lines.append(self.indent + text + '\n')
    
    def openScope(self):
        self.write(self.openTag)
        self.indent += self.tab

    def closeScope(self):
        self.indent = self.indent[:-len(self.tab)]
        self.write(self.closeTag)
    
    def getContents(self, indent=''):
        return ('').join([indent + line for line in self.lines])

    def activate(self):   self.active = True
    
    def deactivate(self): self.active = False