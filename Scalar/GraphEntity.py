from .Graph import Graph

class GraphEntity:
    
    graph = Graph()

    @property
    def forward(self): return self.graph.forwardBuffer
    
    @property
    def reverse(self): return self.graph.reverseBuffer