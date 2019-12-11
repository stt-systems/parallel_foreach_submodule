# -*- coding: utf-8 -*-

import subprocess as sub
import os


class PFSProcess(object):
    def __init__(self, submodule, path, cmd, counter, output_filter="", cmd_func=None, output_func=None):
        self.__submodule = submodule
        self.__path = path
        self.__cwd = os.path.join(self.__path, self.__submodule)
        self.__cmd = cmd
        self.__counter = counter
        self.__output_filter = output_filter
        self.__active_branch = self.get_current_branch(self.__cwd)[:-1]
        self.__cmd_func = cmd_func
        self.__output_func = output_func
        self.__output = None
        self.__ret = None
        self.__p = None

    @staticmethod
    def get_current_branch(path):
        return sub.check_output(['git', '-C', path, 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8')

    def run(self):
        is_empty = True
        self.__output = "\n\n" + self.__submodule + "\n"
        # self.__output = sub.check_output(self.__cmd)
        if self.__cmd_func:
            self.__cmd = self.__cmd_func(self.__cmd, self.__active_branch)
        self.__p = sub.Popen(self.__cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True,
                             cwd=os.path.join(self.__path, self.__submodule))

        #print(self.__cmd)
        #print(self.__p.communicate()[0].decode('utf-8'))
        if self.__p.communicate()[0].decode('utf-8') != '':
            self.__ret = self.__p.communicate()[0].decode('utf-8')  # stdoutdata
            if self.__output_func:
                self.__ret = self.__output_func(self.__ret)
            self.__output += self.__ret
            is_empty = False

        if self.__p.communicate()[1]:  # stderrdata
            self.__output += self.__p.communicate()[1].decode('utf-8')

        self.__output += str(self.__counter.increment_value())

        if self.__output_filter == "":
            print(self.__output)
        else:
            if str(self.__output).find(self.__output_filter) == -1 and self.__output_filter != '@<empty>@' \
                    or (str(self.__output).find(self.__output_filter) == -1
                        and self.__output_filter == '@<empty>@' and not is_empty):
                print(self.__output)
