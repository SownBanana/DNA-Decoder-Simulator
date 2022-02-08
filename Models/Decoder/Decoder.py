from utils import pivot
import random


def sort_func(vertex):
    return vertex.weight()


class DecoderAlgo:
    def __init__(self, min_weight):
        self.queue = []
        self.stack = []
        self.paths = {}
        self.path = []
        self.dictqueue = {}
        self.min_weight = min_weight

    def traversal(self, graph):
        pass

    def get_string_key(self, path):
        k = ''
        for v in path:
            k += v.vertex
        return k

    def check_vertex_not_in_adjacent(self, vertex, adj):
        kmer_size = self.graph.kmer_size
        for v in adj:
            if vertex[:kmer_size] == v[:kmer_size]:
                return False
        return True
    
    def check_key_visited(self, d, key):
        kmer = self.graph.kmer_size
        for k, v in d.items():
            if key.startswith(k) and key[-kmer:] == k[-kmer:]:
                return v
        return False


class BFS(DecoderAlgo):
    def __init__(self, min_weight=0, db=0):
        self.db = db
        DecoderAlgo.__init__(self, min_weight)

    def traversal(self, graph):
        self.graph = graph
        kmer_size = self.graph.kmer_size
        for v_key, v in graph.vertexes.items():
            if v_key.startswith(pivot.start) and v.weight() > self.min_weight:
                self.queue.append([v.vertex + '1'])
        dbi = 1
        while self.queue:
            if self.db and dbi % self.db == 0:
                print(len(self.queue[-1]), len(self.queue))
            dbi += 1
            path = self.queue.pop(0)
            key = ''.join(path)
            end_v = path[-1][:kmer_size]
            adj_v = []
            v = self.graph.get_next_vertex(end_v)
            c = 1
            while v:
                if not self.check_key_visited(v.visited, key) \
                        and self.check_vertex_not_in_adjacent(v.vertex, adj_v) \
                        and self.graph.get_vertex_with_weight(v).weight() > self.min_weight:
                    v.visited.update({key: True})
                    adj_v.append(v.vertex + str(c))
                    c += 1
                v = v.next
            for v in adj_v:
                p = path.copy()
                p[-1] = p[-1][:kmer_size] + v[kmer_size:]
                p.append(v)
                if len(p) == self.graph.v_num:
                    if v[:-1].endswith(pivot.stop):
                        pnn = ''
                        for i in range(len(p) - 1):
                            pnn += p[i][0]
                        pnn += p[-1][:-1]
                        self.path.append(pnn)
                else:
                    self.queue.append(p)
        return self.path


class DFS(DecoderAlgo):
    def __init__(self, min_weight=0):
        DecoderAlgo.__init__(self, min_weight)

    def traversal(self, graph):
        self.graph = graph
        for v_key, v in graph.vertexes.items():
            if v_key.startswith(pivot.start):
                self.stack.append(v)
        self.stack.sort(key=sort_func)

        while self.stack or len(self.path) < self.graph.v_num:
            v = self.stack.pop()
            self.path.append(v.vertex)
            adj_vs = []
            v = self.graph.get_next_vertex(v)
            while v:
                # if v
                adj_vs.append(self.graph.get_vertex_with_weight(v))
                v = v.next
            adj_vs.sort(key=sort_func)
            self.stack.extend(adj_vs)
            print(len(self.path), self.path)
