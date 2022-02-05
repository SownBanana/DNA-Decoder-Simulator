class Node:
    def __init__(self, value):
        self.vertex = value
        self.w_in = 0
        self.w_out = 0
        self.next = None
        self.visited = {}

    def next(self, node):
        self.next = node
    
    def edge_in(self):
        self.w_in += 1

    def edge_out(self):
        self.w_out += 1
    
    def weight(self):
        i = self.w_in if self.w_in > 0 else self.w_out
        o = self.w_out if self.w_out > 0 else self.w_in

        return (i+o)/2

    def visit(self, index='one_way'):
        self.visited.update({index: True})
    
    def has(self, node):
        n = self
        while n:
            if n.vertex == node:
                return True
            n = n.next
        return False

    def __repr__(self):
        node = self.next
        s = str(self.vertex)
        while node:
            s += " -> {}".format(node.vertex)
            node = node.next
        return s
