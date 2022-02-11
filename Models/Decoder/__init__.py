from Models.DeBruijn.Graph import Graph
from Models.Decoder.Decoder import DFS
class Decoder():
    def __init__(self, origin = None, minimize_edge=True, prune=0, *args, **kwargs):
        self.minimize_edge = minimize_edge
        self.origin = origin
        self.prune = prune
    
    def build_graph(self, data, original_length, kmer_size=4, visualization=False):
        self.data_length = original_length
        self.graph = Graph(data = data, data_length=original_length, kmer_size=kmer_size, prune=self.prune)
        self.graph.build()
        self.graph.origin = self.origin
        if visualization:
            self.graph.draw_de_bruijn_graph(minimize_edge=self.minimize_edge)

    def decode(self, algo=None):
        assert not self.graph is None, 'Graph is not initialized'
        if algo is None:
            algo = DFS(min_weight=self.prune)
        paths = algo.traversal(self.graph)
        check = False
        for path in paths:
            if path == self.origin:
                check = True
                break
        return check, paths
        # for v in self.graph.vertexes:
        #     print(v)