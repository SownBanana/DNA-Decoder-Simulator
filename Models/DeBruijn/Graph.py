from Models.DeBruijn.Node import Node

class Graph:
    def __init__(self, data, data_length=200, kmer_size=4, head=None, tail=None):
        self.data_length = data_length
        self.graph = {}
        self.vertexes = {}
        self.head = head
        self.tail = tail
        self.phase = 'build'
        self.datas = data
        self.is_2_way = False
        self.kmer_size = kmer_size
        # assert data_length % kmer_size == 0, f'data_length={data_length} is not divisible by kmer_size={kmer_size}'
        self.v_num = data_length//kmer_size
        self.build_visited = {}

    def set_phase(self, phase='traversal'):
        self.phase = phase

    def config(self, kmer_size=4, is_2_way=False, head=None, tail=None):
        self.kmer_size = kmer_size
        self.is_2_way = is_2_way
        self.head = head
        self.tail = tail

    def get_vertexes(self):
        return [kmer for kmer, _ in self.vertexes.items()]

    def b_visit(self, src, dst, key):
        i = src+dst
        if not i in self.build_visited:
            self.build_visited.update({i: key})
        else:
            self.build_visited[i] = key

    def add_edge(self, src, dst, key=0):
        dst_node = Node(dst)

        if src in self.graph:
            if not self.graph[src].has(dst) \
                    or ((src+dst) in self.build_visited and self.build_visited[src+dst] == key):
                dst_node.next = self.graph[src]
                self.graph[src] = dst_node
            if not dst in self.vertexes:
                self.vertexes.update({dst: dst_node})
            self.vertexes[src].edge_out()
            self.vertexes[dst].edge_in()
        else:
            self.graph.update({src: dst_node})

            if not src in self.vertexes:
                src_node = Node(src)
                self.vertexes.update({src: src_node})
            else:
                src_node = self.vertexes[src]

            if not dst in self.vertexes:
                dst_node = Node(dst)
                self.vertexes.update({dst: dst_node})
            else:
                dst_node = self.vertexes[dst]

            self.vertexes[src].edge_out()
            self.vertexes[dst].edge_in()

        self.b_visit(src, dst, key)

    def build(self):
        key = 1
        for data in self.datas:
            kmers = [data[i:i+self.kmer_size]
                     for i in range(0, len(data) - self.kmer_size + 1)]
            for i in range(0, len(kmers) - 1):
                self.add_edge(kmers[i], kmers[i+1], key=key)
            key += 1
        self.build_visited = {}

    def __repr__(self):
        s = ""
        for kmer, node in self.vertexes.items():
            if kmer in self.graph:
                node = self.graph[kmer]
            else:
                tmp = node
                node = Node(None)
                node.w_in
            s += "Vertex " + str(kmer) + " - " + \
                str(self.vertexes[kmer].weight(
                )) + f"({self.vertexes[kmer].w_in}, {self.vertexes[kmer].w_out})" + ": "
            s += str(node)
            s += " \n"
        return s
