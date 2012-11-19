from heapq import *

import sys
sys.path.insert(0, '..')

from const.constants import *
from graph import make_graph


class Dijkstra(object):
    """This class is designed for solving general graphs without
    negative weighted edges, not limited to grid maps.
    """

    def __init__(self, graph, source, target):
        """Create a new instance of Dijkstra path finder.

        :Parameters:
            graph : {nodeid1: {nodeid2: dist, ... }, ... }
                The graph is in ajacency list representation.
                The nodeid can be any hashable object.
                Sample graphs are as follows:
                    graph = {(1, 2): {(2, 2): 1, (1, 3): 1},
                             (2, 2): {(1, 2): 1},
                             (1, 3): {(1, 2): 1}}
                or
                    graph = {'A': {'B': 1, 'C': 1},
                             'B': {'A': 1},
                             'C': {'A': 1}}

            source : nodeid
                Source coordinate.

            target : nodeid
                Destination coordinate.
        """
        self.graph = graph
        self.source = source
        self.target = target
        self.path = []

        # record of each node's parent
        self.parent = {}

        # record of each node's estimate distance
        self.dist = dict([(pos, INF) for pos in graph])

        # set of open nodes
        self.nodes = set([pos for pos in graph])

    def step(self, record = None):
        """Starts the computation of shortest path.
        :Parametes:
            record : deque
                if a queue is specified, a record of each operation
                (OPEN, CLOSE, etc) will be pushed into the queue.
        """
        self.dist[self.source] = 0
        while self.dist:
            # get the node with minimum estimated distance
            node = min(self.nodes, key = self.dist.__getitem__)
            self.nodes.remove(node)

            if record != None:
                record.append(('CLOSE', node))

            # if the node with minimum estimated distance has the
            # distance of infinity, then there is no such path from
            # source to distance.
            if self.dist[node] == INF:
                break

            # if the node is the target, then the path exists.
            if node == self.target:
                self._retrace()
                break

            # inspect the adjacent nodes.
            for adj in self.graph[node]:
                if adj in self.nodes:
                    self._relax(node, adj, record)
                    if record != None:
                        record.append(('OPEN', adj))
            yield
        yield


    def _relax(self, u, v, record_):
        """Relax an edge.
        :Parameters:
            u : nodeid
                Node u
            v : nodeid
                Node v
        :Return:
            suc : bool
                whether the node v can be accessed with a lower
                cost from u.
        """
        d = self.dist[u] + self.graph[u][v]
        if d < self.dist[v]:
            self.dist[v] = d
            self.parent[v] = u
            if record_ != None:
                record_.append(('VALUE', ('f', v, d)))
                record_.append(('PARENT', (v, u)))
            return True
        return False


    def _retrace(self):
        """This method will reconstruct the path according to the
        nodes' parents.
        """
        self.path = [self.target]
        while self.path[-1] != self.source:
            self.path.append(self.parent[self.path[-1]])
        self.path.reverse()



class GridDijkstra(Dijkstra):
    """This class is specified to grid maps.

    *Note*: On grid maps with all horizontal and vertical weights
    set to be 10 and all diagonal weights set to be 14, like
    we presumed in this scenario, Dijkstra's algorithm explores
    nodes in exactly the same way as a generic Breadth-First-Search
    algorithm.
    """
    def __init__(self, raw_graph):
        g, s, t = make_graph(raw_graph)
        Dijkstra.__init__(self, g, s, t)


def _test():
    nodes_map_raw = '''
                    S0000000000000000000000000100000000000
                    00000000000000000000110000010000000000
                    00000000000000000000100000001000000000
                    10000111110101000001100000001000000000
                    01111100010001000010100000010000000000
                    00000100001111100100100001110000110000
                    00001100000001011000000100000001000000
                    00000100000000101000000000011110000001
                    00000010000000000111111111100000000011
                    00000001000000000000000001100000111100
                    00000000110000000000000000010011000000
                    00000000010000000001100000001000000000
                    00000000010000000000110000000111111000
                    00000000010000000000010000000000000000
                    00000000011000111111111111111111111111
                    000000000100000110000010000000000000T0
                    00000000001100000100001000000000000000
                    00000000000100000011000000000000000000
                    00000000000010000000000000000000000000
                    '''
    graph2 = [list(row) for row in nodes_map_raw.split()]
    nr = len(graph2)
    nc = len(graph2[0])
    dij = GridDijkstra(nodes_map_raw)
    for i in dij.step():
        pass
    if dij.path:
        for y in xrange(nr):
            for x in xrange(nc):
                if (x, y) == dij.source:
                    print 'S',
                elif (x, y) == dij.target:
                    print 'T',
                elif (x, y) in dij.path:
                    print '.',
                elif graph2[y][x] == BLOCKED:
                    print 'X',
                else:
                    print ' ',
            print
        print 'Route length:', len(dij.path)
    else:
        print 'Failed to find the path'

if __name__ == '__main__':
    from cProfile import Profile
    p = Profile()
    p.runcall(_test)
    p.print_stats(sort = 1)
