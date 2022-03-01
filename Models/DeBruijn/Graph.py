import networkx as nx
import matplotlib.pyplot as plt
from Models.DeBruijn.Node import Node
import numpy as np
import math

class Graph:

    def __init__(self, data, data_length=200, kmer_size=4, head=None, tail=None, prune=0):
        self.build_visited = {}
        self.g_vis = nx.DiGraph()
        self.g_vis_pruned = nx.DiGraph()
        self.graph = {}
        self.vertexes = {}
        self.is_2_way = False
        self.phase = 'build'
        
        self.data_length = data_length
        self.head = head
        self.tail = tail
        self.datas = data
        self.kmer_size = kmer_size
        # assert data_length % kmer_size == 0, f'data_length={data_length} is not divisible by kmer_size={kmer_size}'
        self.v_num = data_length - kmer_size + 1
        self.prune = prune

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

    def _update_edge_weight(self, src, dst):
        self.vertexes[src].edge_out()
        self.vertexes[dst].edge_in()
        self.g_vis.add_edge(src, dst, weight=self.vertexes[dst].w_in)
        if self.vertexes[dst].weight() > self.prune:
            self.g_vis_pruned.add_edge(src, dst, weight=self.vertexes[dst].w_in)

    def _add_new_vertex(self, src, dst, dst_node):
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

    def add_edge(self, src, dst, key=0):
        dst_node = Node(dst)

        if src in self.graph:
            if not self.graph[src].has(dst) \
                    or ((src+dst) in self.build_visited and self.build_visited[src+dst] == key):
                dst_node.next = self.graph[src]
                self.graph[src] = dst_node
            if not dst in self.vertexes:
                self.vertexes.update({dst: dst_node})
        else:
            self._add_new_vertex(src, dst, dst_node)

        self._update_edge_weight(src, dst)
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

    def get_next_vertex(self, v):
        if type(v) is str:
            if v in self.graph:
                return self.graph[v]
            return None
        if v.vertex in self.graph:
            return self.graph[v.vertex]
        return None
    
    def get_vertex_with_weight(self, v):
        if type(v) is str:
            if v in self.vertexes:
                return self.vertexes[v]
            return None
        if v.vertex in self.vertexes:
            return self.vertexes[v.vertex]
        return None

    def __repr__(self):
        s = ""
        for kmer, node in self.vertexes.items():
            if kmer in self.graph:
                node = self.graph[kmer]
            else:
                node = Node(None)
            s += "Vertex " + str(kmer) + " - " + \
                str(self.vertexes[kmer].weight(
                )) + f"({self.vertexes[kmer].w_in}, {self.vertexes[kmer].w_out})" + ": "
            s += str(node)
            s += " \n"
        return s

    def draw_de_bruijn_graph(self, weight_on=False, thickness=True, minimize_edge=False, font_color='k', node_size=800, weight_scale=1, font_size=6, pruned=False,figsize=(15,15)):
        g = self.g_vis
        if pruned:
            g = self.g_vis_pruned
        weights = None
        if thickness:
            edges = g.edges()
            weights = [g[u][v]['weight'] for u,v in edges]
            weights = np.array(weights)
            if minimize_edge:
                weights = weights / np.average(weights)
            weights = weights*weight_scale

        plt.figure(figsize=figsize)
        #555555
        #9ED0FD - light blue
        
        nx.draw_networkx(
            g, pos=nx.kamada_kawai_layout(g),
            node_shape='o', node_size=node_size, font_size=font_size,
            edge_color='#555555', width=weights, font_color=font_color
        )
        if weight_on:
            nx.draw_networkx_edge_labels(
                g, pos=nx.kamada_kawai_layout(g), 
                edge_labels=nx.get_edge_attributes(g, 'weight'),
                font_size=font_size+2, label_pos=0.5, rotate=False,
            )
        plt.axis('off')
        plt.show() 