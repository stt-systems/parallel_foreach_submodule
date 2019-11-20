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


def worker(submodule_list, path, command, counter, output_filter="", cmd_func=None, output_func=None):
    if isinstance(submodule_list, Scheduler):
        while not submodule_list.empty():
            PFSProcess(submodule_list.get(), path, command, counter, output_filter, cmd_func, output_func).run()
    else:
        for submodule in submodule_list:
            PFSProcess(submodule, path, command, counter, output_filter, cmd_func, output_func).run()


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
        parser.add_argument('--pull', dest='pull', action='store_true',
                            help='Shortcut to "git pull origin"')
        parser.add_argument('--pending', dest='pending', action='store_true',
                            help='Shortcut to "git log <since origin/current>..<until current>"')
        parser.add_argument('--status', dest='status', action='store_true',
                            help='Shortcut to "git status"')
        parser.add_argument('--in-branch', dest='in_branch',
                            help='Shortcut to "IF (git rev-parse --abbrev-ref HEAD) == branch"')
        parser.add_argument('--verbose', dest='verbose', action='store_true',
                            help='Verbose option in shortcuts')
        self.args = parser.parse_args()

        self.__cmd_alias = {
            'pull': ('git pull origin', 'Already up to date', None, None),
            'status': ('git status', 'nothing to commit', None, None),
            'pending': ('git log origin/@Abranch@..@Abranch@', '@<empty>@',
                        lambda cmd, tag_value: str(cmd).replace('@Abranch@', tag_value, 2), None),
            'in_branch': ('git rev-parse --abbrev-ref HEAD', 'OTHER', None,
                          lambda output: "In " + output[:-1] + " branch\n"
                          if str(output[:-1]).find(self.args.in_branch) != -1 else "In OTHER branch -> " + output),
            'not_in_branch': ('git rev-parse --abbrev-ref HEAD', 'OTHER', None,
                              lambda output: "Not in " + output[:-1] + " branch\n"
                              if str(output)[:-1].find(self.args.not_in_branch) == -1 else "In OTHER branch -> " + output),
        }

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
        command_function = None
        output_function = None
        if self.args.pull:
            command = self.__cmd_alias["pull"][0]
            if not self.args.verbose:
                output_filter = self.__cmd_alias["pull"][1]
            command_function = self.__cmd_alias["pull"][2]
            output_function = self.__cmd_alias["pull"][3]
        if self.args.status:
            command = self.__cmd_alias["status"][0]
            if not self.args.verbose:
                output_filter = self.__cmd_alias["status"][1]
            command_function = self.__cmd_alias["status"][2]
            output_function = self.__cmd_alias["pull"][3]
        if self.args.pending:
            command = self.__cmd_alias["pending"][0]
            if not self.args.verbose:
                output_filter = self.__cmd_alias["pending"][1]
            command_function = self.__cmd_alias["pending"][2]
            output_function = self.__cmd_alias["pull"][3]
        if self.args.in_branch:
            command = self.__cmd_alias["in_branch"][0]
            if not self.args.verbose:
                output_filter = self.__cmd_alias["in_branch"][1]
            command_function = self.__cmd_alias["in_branch"][2]
            output_function = self.__cmd_alias["in_branch"][3]
        try:
            self.empty_cmd(command)
        except argparse.ArgumentTypeError as e:
            print(e)
            exit(0)

        for i in range(self.args.jobs):
            if self.args.schedule == "load-share":
                t = threading.Thread(target=worker,
                                     args=(scheduler, self.args.path, command, self.__counter,
                                           output_filter, command_function, output_function,))
            else:
                t = threading.Thread(target=worker,
                                     args=(list_submodule_list[i], self.args.path, command, self.__counter,
                                           output_filter, command_function, output_function,))
            self.__threads.append(t)
            t.start()

        for i in range(self.args.jobs):
            self.__threads[i].join()

        print("\nExecution complete!")
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    pfs = PFS()
    pfs.run()
