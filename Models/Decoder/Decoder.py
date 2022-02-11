from utils import pivot
import math


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
        if not adj:
            return True
        kmer_size = self.graph.kmer_size
        if type(adj[0]) is str:
            for v in adj:
                if vertex[:kmer_size] == v[:kmer_size]:
                    return False
            return True
        for v in adj:
            if vertex.vertex[:kmer_size] == v.vertex[:kmer_size]:
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
                if self.graph.get_vertex_with_weight(v).weight() > self.min_weight \
                    and not self.check_key_visited(v.visited, key) \
                        and self.check_vertex_not_in_adjacent(v.vertex, adj_v):
                    v.visited.update({key: True})
                    adj_v.append(v.vertex + str(c))
                    c += 1
                v = v.next
            for v in adj_v:
                p = path.copy()
                p[-1] = p[-1][:kmer_size] + v[kmer_size:]
                p.append(v)
                if len(p) == self.graph.v_num:
                    if v[:kmer_size].endswith(pivot.stop):
                        pnn = ''
                        for i in range(len(p) - 1):
                            pnn += p[i][0]
                        pnn += v[:kmer_size]
                        self.path.append(pnn)
                else:
                    self.queue.append(p)
        return self.path


class Path:
    def __init__(self, vertexes=[], weight=0):
        self.vertexes = vertexes
        self.w = weight

    def copy(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.vertexes = self.vertexes.copy()
        result.w = self.w
        return result

    def __repr__(self):
        return ''.join(self.vertexes)

    def weight(self):
        return math.ceil(self.w / len(self.vertexes))

    def avg_weight(self):
        return self.w / len(self.vertexes)


class Beam(DecoderAlgo):
    def __init__(self, k, min_weight=0, db=0):
        self.k = k
        self.db = db
        DecoderAlgo.__init__(self, min_weight)

    def traversal(self, graph):
        self.graph = graph
        kmer_size = self.graph.kmer_size

        next_v = []

        for v_key, v in graph.vertexes.items():
            if v_key.startswith(pivot.start):
                next_v.append(v)

        next_v.sort(key=sort_func, reverse=True)

        for i in range(min(len(next_v), self.k)):
            self.queue.append(
                Path([next_v[i].vertex + '1'], next_v[i].weight()))

        dbi = 1

        while self.queue:
            if self.db and dbi % self.db == 0:
                print(len(self.queue[-1].vertexes), len(self.queue))
            dbi += 1
            temp_queue = []
            for path in self.queue:
                key = ''.join(path.vertexes)
                end_v = path.vertexes[-1][:kmer_size]
                adj_v = []
                v = self.graph.get_next_vertex(end_v)
                while v:
                    if not self.check_key_visited(v.visited, key) \
                            and self.check_vertex_not_in_adjacent(v, adj_v):
                        v.visited.update({key: True})
                        adj_v.append(self.graph.get_vertex_with_weight(v))
                    v = v.next

                adj_v.sort(key=sort_func, reverse=True)

                c = 1
                for v in adj_v:
                    p = path.copy()
                    p.vertexes[-1] = p.vertexes[-1][:kmer_size] + str(c)
                    p.vertexes.append(v.vertex + str(c))
                    p.w += v.weight()
                    temp_queue.append(p)
                    c += 1

            self.queue = []
            temp_queue.sort(key=sort_func, reverse=True)
            for i in range(min(len(temp_queue), self.k)):
                p = temp_queue[i]
                end_v = p.vertexes[-1][:kmer_size]
                if len(p.vertexes) == self.graph.v_num:
                    if end_v.endswith(pivot.stop):
                        pnn = ''
                        for i in range(len(p.vertexes) - 1):
                            pnn += p.vertexes[i][0]
                        pnn += end_v
                        self.path.append(pnn)
                else:
                    self.queue.append(p)

        return self.path


class DFS(DecoderAlgo):
    def __init__(self, min_weight=0):
        DecoderAlgo.__init__(self, min_weight)

    def traversal(self, graph):
        self.graph = graph
        kmer_size = self.graph.kmer_size
        for v_key, v in graph.vertexes.items():
            if v_key.startswith(pivot.start) and v.weight() > self.min_weight:
                self.stack.append(Path([v.vertex + '1'], v.weight()))
        self.stack.sort(key=sort_func)

        while self.stack:
            path = self.stack.pop()
            key = ''.join(path.vertexes)
            end_v = path.vertexes[-1][:kmer_size]
            adj_v = []
            v = self.graph.get_next_vertex(end_v)
            while v:
                vw = self.graph.get_vertex_with_weight(v)
                if self.graph.get_vertex_with_weight(v).weight() > self.min_weight \
                    and not self.check_key_visited(v.visited, key) \
                    and self.check_vertex_not_in_adjacent(v, adj_v):
                    v.visited.update({key: True})
                    adj_v.append(self.graph.get_vertex_with_weight(v))
                v = v.next

            adj_v.sort(key=sort_func)

            c = 1
            for v in adj_v:
                p = path.copy()
                p.vertexes[-1] = p.vertexes[-1][:kmer_size] + str(c)
                p.vertexes.append(v.vertex + str(c))
                p.w += v.weight()

                if len(p.vertexes) == self.graph.v_num:
                    if v.vertex.endswith(pivot.stop):
                        pnn = ''
                        for i in range(len(p.vertexes) - 1):
                            pnn += p.vertexes[i][0]
                        pnn += v.vertex
                        self.path.append(pnn)
                        if pnn == self.graph.origin:
                            return self.path
                else:
                    self.stack.append(p)

                c += 1

        return self.path
