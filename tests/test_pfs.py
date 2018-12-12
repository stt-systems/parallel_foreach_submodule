# -*- coding: utf-8 -*-

import unittest
import subprocess as sub
import os


def git(*args):
    return sub.check_call(['git'] + list(args))


class TestPFS(unittest.TestCase):

    def setUp(self):
        print(sub.check_call(['pfs', '--help']))
        git("clone", "https://github.com/RDCH106/git_submodules_test_project.git",
            os.path.dirname(os.path.abspath(__file__))+"/tmp/git_submodules_test_project", "--recursive")

    def tearDown(self):
        if os.name == 'nt':  # on windows
            os.system("rmdir /s /q " + os.path.dirname(os.path.abspath(__file__))+"\\tmp\\git_submodules_test_project")
        else:  # on linux / os x
            os.system("rm - rf " + os.path.dirname(os.path.abspath(__file__)) + "/tmp/git_submodules_test_project")

    def test_command(self):
        #print(sub.check_call(['cd', os.path.dirname(os.path.abspath(__file__))+'/tmp/git_submodules_test_project', '&&',
        #                      'pfs', '-c', '"git checkout master"']))
        print("hello")


if __name__ == '__main__':
    unittest.main(verbosity=2)

