"""import sys
import subprocess
import time
file_handler = open('ipcd2.dat','w')
file_handler.write(str('13'))
file_handler.close()
print '\nSpawned in Hard-Code Mode\nWriting control instructions to GUIs\nSlavescreen is now running A-Star at speed 16X'
file_handler = open('ipcd1.dat','w')
file_handler.write(str('33'))
file_handler.close()
print '\nMasterscreen is now running Dijkstra at 16X'
"""
import os
import sys
import subprocess
import threading
from Tkinter import *
import sociopath_client

class ControllerRow(Frame):

    ALGORITHM_OPTIONS = [
        "A* (Manhattan)",
        "A* (Euclidean)",
        "A* (Chebyshev)",
        "Uniform Cost",
        "Dijkstra",
        "Bi-Directional BFS"
    ]

    SPEED_OPTIONS = [
        "1 x",
        "2 x",
        "4 x",
        "8 x",
        "16 x",
        "32 x",
        "64 x",
        "128 x",
        "256 x",
        "512 x"
    ]
    """
        "1024 x",
        "2048 x",
        "4096 x"
    ]"""

    def __init__(self, parent, number = 0):

        Frame.__init__(self)
        self.number = number

        self.label_window = Label(self, text="Window "+str(number))
        self.label_window.grid(row=0,column=0)

        self.algo = StringVar(self)
        self.algo.set(self.ALGORITHM_OPTIONS[0])
        self.options_algo = OptionMenu(self, self.algo, *self.ALGORITHM_OPTIONS)
        self.options_algo.grid(row=0,column=1)

        self.speed = StringVar(self)
        self.speed.set(self.SPEED_OPTIONS[7])
        self.options_speed = OptionMenu(self, self.speed, *self.SPEED_OPTIONS)
        self.options_speed.grid(row=0,column=2)


class SocioPathController:

    WINDOW_OPTIONS = []

    controller_rows = []

    def __init__(self, parent, max_windows = 5):
        self.max_windows = abs(max_windows)
        for i in range(0, self.max_windows):
            self.WINDOW_OPTIONS.append(str(i+1))

        self.num_windows_int = self.max_windows

        self.parent = parent
        self.parent.title("SocioPATH Controller")

        self.label_numwindows = Label(parent, text="Number of windows: ")
        self.label_numwindows.grid(row=0, column=0)

        self.num_windows = StringVar(parent)
        self.num_windows.set(self.WINDOW_OPTIONS[self.num_windows_int-1])
        self.options_windows = OptionMenu(parent, self.num_windows,*self.WINDOW_OPTIONS, command=self.numchanged)
        self.options_windows.grid(row=0, column=1)

        self.launch_button = Button(parent, text="Launch", command=self.launch)
        self.launch_button.grid(row=0, column=2)


        for i in range(0, self.max_windows):
            row = ControllerRow(parent, i)
            row.grid(row=i+1, columnspan=3)
            self.controller_rows.append(row)

    def numchanged(self, args):
        self.num_windows_int = int(args)
        for i in range(0, self.max_windows):
            if i < self.num_windows_int:
                self.controller_rows[i].grid()
            else:
                self.controller_rows[i].grid_remove()

    threads = []

    def launch(self):
        # First stop any threads
        #for t in self.threads:
        #    t.
        for i in range(0, self.num_windows_int):
            file_handler = open('sociopath%s.dat' % (i),'w')
            # Write algorithm number (0-based)
            self.algo = self.controller_rows[i].ALGORITHM_OPTIONS.index(self.controller_rows[i].algo.get())
            file_handler.write( str(self.algo) )
            # Write speed number (0-based)
            self.speed = self.controller_rows[i].SPEED_OPTIONS.index(self.controller_rows[i].speed.get())
            file_handler.write( str(self.speed) )
            file_handler.close()

        #self.host = 'localhost'
        #self.port = 31416
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.client_path = os.path.join(self.cur_path, 'sociopath_client.py')

        # Launch client windows
        for i in range(0, self.num_windows_int):
            #self.c = sociopath_client.Client(self.ui_path, (self.host, self.port), i)
            #self.threads.append(threading.Thread(target=self.c.run))
            #self.threads[-1].start()

            self.p = subprocess.Popen(['python', self.client_path, '-n', str(i)])
            #self.p.kill()

def main():
    root = Tk()
    controller = SocioPathController(root)
    root.mainloop()


if __name__ == '__main__':
    main()

