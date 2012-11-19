from heapq import *

import sys
sys.path.insert(0, '..')

from graph import is_walkable, InvalidMap
from const.constants import *

class _Node(object):
    """This class works as the container of the nodes' info.
    """
    def __init__(self, status):
        self.g = None # cost from source
        self.h = None # cost from target
        self.parent = None
        self.visited_by = None
        self.status = status


class BiDirBFS(object):
    """ Bi-Directional Breadth-First-Search.
    Explores the map simultaneously from source and target. When the two
    trees meet, a shortest path is found.

    *NOTE* This class is designed for solving graphs with equal
    weighted edges. That is to say, on graphs with various weights,
    this algorithm doesn't gurantee to find the shortest path.
    """

    def __init__(self, raw_graph):
        """Create a new instance of Bi-Directional Breadth-First-Search
        path finder.

        :Parameters:
            raw_graph : str
                A multi-line string representing the graph.
                example:
                s = '''
                    S000
                    1110
                    T000
                    '''
        """
        self.graph = raw_graph.split()
        self.n_row = len(self.graph)
        self.n_col = len(self.graph[0])
        self.source = None
        self.target = None
        self.path = []
        self.success = False

        # nodes grid
        self.nodes = [[_Node(self.graph[y][x])
                        for x in xrange(self.n_col)]
                            for y in xrange(self.n_row)]

        # get source and target coordinates
        for y in xrange(self.n_row):
            for x in xrange(self.n_col):
                if self.graph[y][x] == SOURCE:
                    self.source = (x, y)
                elif self.graph[y][x] == TARGET:
                    self.target = (x, y)
        if not all((self.source, self.target)):
            raise InvalidMap('No source or target given')


        self.queue_source = []
        self.queue_target = []


    def step(self, record = None):
        """Starts the computation of shortest path.
        :Parametes:
            record : deque
                if a queue is specified, a record of each operation
                (OPEN, CLOSE, etc) will be pushed into the queue.
        """
        # push the source node into the source queue and the
        # target node into the target queue
        sx, sy = self.source
        tx, ty = self.target
        self.queue_source.append((0, self.source))
        self.queue_target.append((0, self.target))
        self.nodes[sy][sx].g = 0
        self.nodes[ty][tx].h = 0
        self.nodes[sy][sx].visited_by = CSOURCE
        self.nodes[ty][tx].visited_by = CTARGET

        # while both source queue and target queue is not empty
        # expand them.
        while self.queue_source and self.queue_target and \
                not self.success:
            self._expand_source(record)
            if self.success:
                break
            yield
            self._expand_target(record)
            yield
        yield



    def _expand_source(self, rec):
        """Searches from the source. Until it meets a node which
        has been visited by the other tree.
        """
        # take the first node from the source queue
        v, (x, y) = heappop(self.queue_source)
        node = self.nodes[y][x]

        diagonal_can = [] # stores the diagonal positions that can be accessed

        if rec != None:
            rec.append(('CLOSE', (x, y)))

        # inspect horizontally and vertically adjacent nodes
        for i in xrange(len(XOFFSET)):
            nx = x + XOFFSET[i]
            ny = y + YOFFSET[i]
            if is_walkable(nx, ny, self.n_row, self.n_col,
                    self.graph):
                # if this node can be accessed, then then correponding
                # diagonal node can be accessed.
                diagonal_can.append(i)

                nxt_node = self.nodes[ny][nx]
                # if this node has been visited by source queue before,
                # then there's no need to inspect it again.
                if nxt_node.visited_by == CSOURCE:
                    continue

                # if this node has been visited by *target* queue.
                # Then a path from source to target exists.
                # Reconstructs the path and return.
                if nxt_node.visited_by == CTARGET:
                    if rec:
                        rec.append(('CLOSE', (nx, ny)))
                    self._retrace((x, y), (nx, ny))
                    self.success = True
                    return

                # mark this node and update its info, then push the node
                # into the source queue
                nxt_node.visited_by = CSOURCE
                nxt_node.g = node.g + DIST
                nxt_node.parent = (x, y)
                heappush(self.queue_source, (nxt_node.g, (nx, ny)))

                if rec != None:
                    rec.append(('OPEN', (nx, ny)))
                    rec.append(('VALUE', ('g', (nx, ny), nxt_node.g)))
                    rec.append(('PARENT', ((nx, ny), (x, y))))

        # further investigate the diagonal nodes, the procedure is identical
        # with above
        for i in diagonal_can:
            nx1 = x + DAXOFFSET[i]
            ny1 = y + DAYOFFSET[i]
            nx2 = x + DBXOFFSET[i]
            ny2 = y + DBYOFFSET[i]
            npos = ((nx1, ny1), (nx2, ny2))
            for nx, ny in npos:
                if is_walkable(nx, ny, self.n_row, self.n_col,
                     self.graph) and \
                     self.nodes[ny][nx].visited_by != CSOURCE:
                    nxt_node = self.nodes[ny][nx]
                    if nxt_node.visited_by == CTARGET:
                        if rec:
                            rec.append(('CLOSE', (nx, ny)))
                        self._retrace((x, y), (nx, ny))
                        self.success = True
                        return
                    nxt_node.visited_by = CSOURCE
                    nxt_node.g = node.g + DDIST
                    nxt_node.parent = (x, y)
                    heappush(self.queue_source, (nxt_node.g, (nx, ny)))
                    if rec != None:
                        rec.append(('OPEN', (nx, ny)))
                        rec.append(('VALUE', ('g', (nx, ny),
                            nxt_node.g)))
                        rec.append(('PARENT', ((nx, ny), (x, y))))



    def _expand_target(self, rec):
        """Searches from the target. Until it meets a node which
        has been visited by the other tree.
        """
        # the procedure is identical with _expand_source.
        v, (x, y) = heappop(self.queue_target)
        node = self.nodes[y][x]
        diagonal_can = []
        if rec != None:
            rec.append(('CLOSE', (x, y)))
        for i in xrange(len(XOFFSET)):
            nx = x + XOFFSET[i]
            ny = y + YOFFSET[i]
            if is_walkable(nx, ny, self.n_row, self.n_col,
                    self.graph):
                diagonal_can.append(i)
                if self.nodes[ny][nx].visited_by == CTARGET:
                    continue
                nxt_node = self.nodes[ny][nx]
                if nxt_node.visited_by == CSOURCE:
                    if rec:
                        rec.append(('CLOSE', (nx, ny)))
                    self._retrace((nx, ny), (x, y))
                    self.success = True
                    return
                nxt_node.visited_by = CTARGET
                nxt_node.h = node.h + DIST
                nxt_node.parent = (x, y)
                heappush(self.queue_target, (nxt_node.h, (nx, ny)))
                if rec != None:
                    rec.append(('OPEN', (nx, ny)))
                    rec.append(('VALUE', ('h', (nx, ny),
                        nxt_node.h)))
                    rec.append(('PARENT', ((nx, ny), (x, y))))

        # further investigate the diagonal nodes
        for i in diagonal_can:
            nx1 = x + DAXOFFSET[i]
            ny1 = y + DAYOFFSET[i]
            nx2 = x + DBXOFFSET[i]
            ny2 = y + DBYOFFSET[i]
            npos = ((nx1, ny1), (nx2, ny2))
            for nx, ny in npos:
                if is_walkable(nx, ny, self.n_row, self.n_col,
                     self.graph) and \
                     self.nodes[ny][nx].visited_by != CTARGET:
                    nxt_node = self.nodes[ny][nx]
                    if nxt_node.visited_by == CSOURCE:
                        if rec:
                            rec.append(('CLOSE', (nx, ny)))
                        self._retrace((nx, ny), (x, y))
                        self.success = True
                        return
                    nxt_node.visited_by = CTARGET
                    nxt_node.h = node.h + DDIST
                    nxt_node.parent = (x, y)
                    heappush(self.queue_target, (nxt_node.h, (nx, ny)))
                    if rec != None:
                        rec.append(('OPEN', (nx, ny)))
                        rec.append(('VALUE', ('h', (nx, ny),
                            nxt_node.h)))
                        rec.append(('PARENT', ((nx, ny), (x, y))))



    def _retrace(self, s_pos, t_pos):
        """This method will be called when the two search trees meet.
        Since the two trees have different directions, the path must
        be reconstructed seperatedly and then combined.
        """
        s_path = [s_pos]
        t_path = [t_pos]

        while s_path[-1] != self.source:
            x, y = s_path[-1]
            s_path.append(self.nodes[y][x].parent)

        while t_path[-1] != self.target:
            x, y = t_path[-1]
            t_path.append(self.nodes[y][x].parent)

        s_path.reverse()
        self.path = s_path + t_path


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
    bdbfs = BiDirBFS(nodes_map_raw)
    for i in bdbfs.step():
        pass
    if bdbfs.path:
        for y in xrange(nr):
            for x in xrange(nc):
                if (x, y) == bdbfs.source:
                    print 'S',
                elif (x, y) == bdbfs.target:
                    print 'T',
                elif (x, y) in bdbfs.path:
                    print '.',
                elif graph2[y][x] == BLOCKED:
                    print 'X',
                else:
                    print ' ',
            print
        print 'Route length:', len(bdbfs.path)
    else:
        print 'Failed to find the path'

if __name__ == '__main__':
    from cProfile import Profile
    p = Profile()
    p.runcall(_test)
    p.print_stats(sort = 1)
