from Models.DeBruijn.Graph import Graph

class Decoder():
    def __init__(self, minimize_edge=True, *args, **kwargs):
        self.minimize_edge = minimize_edge
    
    def build_graph(self, data, original_length, kmer_size=4, visualization=False):
        self.data_length = original_length
        self.graph = Graph(data = data, data_length=len(original_length), kmer_size=kmer_size)
        self.graph.build()
        if visualization:
            self.graph.draw_de_bruijn_graph(minimize_edge=self.minimize_edge)