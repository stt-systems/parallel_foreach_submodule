# -*- coding: utf-8 -*-

from parallelforeachsubmodule.metadata import Metadata
from parallelforeachsubmodule.process import PFSProcess
from parallelforeachsubmodule.status import Counter
from parallelforeachsubmodule.chunker import split_load
from parallelforeachsubmodule.scheduler import Scheduler
import argparse
import threading
import os
import re
import time
import multiprocessing


def worker(submodule_list, path, command, counter, output_filter=""):
    if isinstance(submodule_list, Scheduler):
        while not submodule_list.empty():
            PFSProcess(submodule_list.get(), path, command, counter, output_filter).run()
    else:
        for submodule in submodule_list:
            PFSProcess(submodule, path, command, counter, output_filter).run()


class PFS(object):
    def __init__(self):
        self.meta = Metadata()
        self.__threads = list()
        self.__counter = None

        # Parse arguments provided
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version=self.meta.get_version())
        parser.add_argument('-p', '--path', dest='path', help='System path where execution starts',
                            type=self.exists_path, default=".")
        parser.add_argument('-c', '--command', dest='command', help='Command to execute',
                            # type=self.empty_cmd,
                            default="")
        parser.add_argument('-s', '--schedule', dest='schedule', help='Scheduling strategy', default='load-share',
                            choices=['CHUNK', 'LOAD-SHARE'],
                            type=lambda s: s.upper())
        parser.add_argument('-j', '--jobs', dest='jobs',
                            help='Number of concurrent jobs. Use -j 0 to use automatically the best maximum number of jobs',
                            type=self.valid_jobs, default=2)
        self.__cmd_alias = {
           'pull': ('git pull origin', 'nothing to commit')
        }
        parser.add_argument('--pull', dest='pull', action='store_true',
                            help='Shortcut to "git pull origin"')
        self.args = parser.parse_args()

        self.__submodule_path_pattern = re.compile('path ?= ?([A-za-z0-9-_]+)(\/[A-za-z0-9-_]+)*([A-za-z0-9-_])')
        self.__path_pattern = re.compile(' ([A-za-z0-9-_]+)(\/[A-za-z0-9-_]+)*([A-za-z0-9-_])')

    @staticmethod
    def exists_path(path):
        if not os.path.isdir(path):
            raise argparse.ArgumentTypeError("%s is not valid path" % path)
        return path

    @staticmethod
    def empty_cmd(cmd):
        if cmd == "":
            raise argparse.ArgumentTypeError("git cmd is empty")
        return cmd

    @staticmethod
    def valid_jobs(jobs):
        if not str(jobs).isdigit():
            raise argparse.ArgumentTypeError("invalid int value: '%s'" % str(jobs))
        if int(jobs) > multiprocessing.cpu_count() * 2:
            raise argparse.ArgumentTypeError("%s jobs are too many jobs for your computer" % str(jobs))
        if int(jobs) == 0:
            return multiprocessing.cpu_count()
        return int(jobs)

    def read_submodules(self, file):
        submodules = list()
        for line in file:
            submodule_path = re.search(self.__submodule_path_pattern, line)
            if submodule_path:
                path = re.search(self.__path_pattern, submodule_path.group())
                if path:
                    submodules.append(path.group()[1:])  # Remove space at first position
        return submodules

    def run(self):
        start_time = time.time()
        if not os.path.exists(os.path.join(self.args.path, '.gitmodules')):
            print("File .gitmodules not found")
            exit(0)

        with open(os.path.join(self.args.path, '.gitmodules')) as f:
            submodules = self.read_submodules(f)

        self.__counter = Counter(len(submodules))
        print(str(len(submodules)) + " submodules")

        if self.args.schedule == "load-share":
            # Load Share Scheduling
            # ----------------------------
            scheduler = Scheduler(submodules)
        else:
            # Chunk Scheduling
            # ----------------------------
            list_submodule_list = split_load(submodules, self.args.jobs)
            # ----------------------------

        #print(list_submodule_list)

        print("Running with " + str(self.args.jobs) + " threads using " + self.args.schedule + " strategy...")

        command = self.args.command
        output_filter = ""
        if self.args.pull:
            command = self.__cmd_alias["pull"][0]
            output_filter = self.__cmd_alias["pull"][1]
        try:
            self.empty_cmd(command)
        except argparse.ArgumentTypeError as e:
            print(e)
            exit(0)

        for i in range(self.args.jobs):
            if self.args.schedule == "load-share":
                t = threading.Thread(target=worker,
                                     args=(scheduler, self.args.path, command, self.__counter, output_filter,))
            else:
                t = threading.Thread(target=worker,
                                     args=(list_submodule_list[i], self.args.path, command, self.__counter, output_filter,))
            self.__threads.append(t)
            t.start()

        for i in range(self.args.jobs):
            self.__threads[i].join()

        print("\nExecution complete!")
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    pfs = PFS()
    pfs.run()
