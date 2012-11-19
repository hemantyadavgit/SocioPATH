"""******************************************************
Author: Hemant Yadav <my-first-name.my-last-name [at] outlook [dot] com>

Description: Server Part for SocioPATH Pathfinder

								  *
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/> """

import os
import sys
import time
import socket
import thread
import cPickle
import asyncore
import functools
import collections

import asynchatmod as asynchat


from algo.astar import *
from algo.dijkstra import *
from algo.bidirbfs import *
from const.constants import *

class MainServer(asyncore.dispatcher):

    def __init__(self, address):
        """Setup main server using the given address
        """
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(5)

        print 'Starting SocioPATH....Preparing Background Resources...Done'
        print 'Spawning GUI Processes....'

    def handle_accept(self):
        """When a new client is connected to the main server, a secondary
        server will be created to handle it.
        """
        sock, addr = self.accept()
        #print 'connected with client at', addr
        SecondaryServer(sock)


class SecondaryServer(asynchat.async_chat):

    def __init__(self, sock):
        """Create a new instance of secondary server to handle
        each client.
        """
        asynchat.async_chat.__init__(self, sock)
        self.peername = self.getpeername()
        #print 'started secondary server'

        self.set_terminator(TERM)

        # incoming data buffer
        self.data = []

        # a flag which will be checked by _step() to determine whether to
        # abort the execution of current algorithm
        self.status = STOPPED

        # command dictionary, dispatches each incomming command
        self.cmd_dict = {'ALGO': self._set_algo,
                         'MAP': self._set_map,
                         'SPEED': self._set_speed,
                         'START': self._start,
                         'STOP': self._stop}

        # algorithm dictionary
        self.algo_dict = {
            'ASTARM':
                functools.partial(AStar, heuristic = MANHATTAN),
            'ASTARE':
                functools.partial(AStar, heuristic = EUCLIDEAN),
            'ASTARC':
                functools.partial(AStar, heuristic = CHEBYSHEV),
            'ASTARU':
                functools.partial(AStar, heuristic = UNIFORMCOST),
            'DIJKSTRA':
                GridDijkstra,
            'BDBFS':
                BiDirBFS}

        self.algo = None
        self.map = None
        self.interval = None


    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        try:
            cmd, arg = cPickle.loads(''.join(self.data))
            self.cmd_dict[cmd](arg)
        except (ValueError, cPickle.UnpicklingError, LookupError), why:
            print why
        finally:
            self.data = []


    def handle_close(self):
        self._stop('')
        print 'disconnected with client at', self.peername
        self.close()

    def _set_algo(self, arg):
        try:
            self.algo = self.algo_dict[arg]
            print 'CMD: set algorithm:'
            print arg
        except (ValueError, LookupError), why:
            print why

    def _set_map(self, arg):
        self.map = arg
        #print 'CMD: set map:'
        #print self.map
        #sys.stdout.write(self.map)
        #file_handler = open('map.txt','w')
        #file_handler.write(str(self.map))
        #file_handler.close()
        #print '\nFile Written!\n'

    def _set_speed(self, arg):
        try:
            speed = arg
            self.interval = 1.0 / speed
            #print 'CMD: set speed:'
            #print '%dX' % speed, '(interval: %lfs)' % self.interval
        except ValueError, why:
            print why

    def _start(self, arg):
        if all((self.algo, self.map, self.interval)):
            self.status = RUNNING
            thread.start_new_thread(self._step, ())
            print 'start calculation ...'

    def _stop(self, arg):
        self.status = STOPPED
        print 'stop'

    def _step(self):
        """This method will be running in a new thread, periodically sending
        the client each step of the algorithm.
        """
        a = self.algo(self.map)
        q = collections.deque()
        for i in a.step(q):
            while q:
                data = cPickle.dumps(q.popleft()) + TERM
                self.push(data)
            time.sleep(self.interval)
            if self.status != RUNNING:
                break
        else:
            # if the algorithm successfully terminated without interrupt,
            # then send the path
            data = cPickle.dumps(('PATH', a.path)) + TERM
            self.push(data)
            self.status = STOPPED


def main(addr):
    server = MainServer(addr)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        server.close()
        print 'quit'


def print_help():
    print """usage: server.py [-p port]
example: server.py -p 27182

The default port is 31416"""


if __name__ == '__main__':
    host = 'localhost'
    port = 31416
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:', ['help'])
        for o, a in opts:
            if o in ('-h', '--help'):
                print_help()
                raise SystemExit
            elif o == '-p':
                port = int(a)
    except (getopt.GetoptError, ValueError):
        #print "Invalid arguments\n"
        print_help()
        raise SystemExit
    main((host, port))
