# -*- coding: utf-8 -*-

import unittest
import subprocess
import os


# https://stackoverflow.com/questions/36169571/python-subprocess-check-call-vs-check-output
def git(*args):
    return subprocess.check_call(['git'] + list(args))


class TestPFS(unittest.TestCase):

    def setUp(self):
        self.sub = subprocess
        print(self.sub.check_call(['pfs', '--version']))
        print(self.sub.check_call(['pfs', '--help']))
        git("clone", "https://github.com/stt-systems/git_submodules_test_project.git",
            os.path.dirname(os.path.abspath(__file__)) + "/tmp/git_submodules_test_project", "--recursive")

    def tearDown(self):
        if os.name == 'nt':  # on windows
            os.system("rmdir /s /q " + os.path.dirname(os.path.abspath(__file__)) + "\\tmp\\git_submodules_test_project")
        else:  # on linux / os x
            os.system("rm -rf " + os.path.dirname(os.path.abspath(__file__)) + "/tmp/git_submodules_test_project")

    def test_command(self):
        if os.name == 'nt':  # on windows
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
        else:  # on linux / os x
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))

    def test_pull_shortcut(self):
        if os.name == 'nt':  # on windows
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs --pull --verbose',
                                        shell=True).decode('utf-8'))
        else:  # on linux / os x
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs --pull --verbose',
                                        shell=True).decode('utf-8'))

    def test_status_shortcut(self):
        if os.name == 'nt':  # on windows
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project\\submodules\\linearizator' +
                                        ' && type nul > change.txt', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs --status --verbose',
                                        shell=True).decode('utf-8'))
        else:  # on linux / os x
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project/submodules/linearizator' +
                                        ' && touch change.txt', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs --status --verbose',
                                        shell=True).decode('utf-8'))

    def test_pending_shortcut(self):
        if os.name == 'nt':  # on windows
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project\\submodules\\linearizator' +
                                        ' && type nul > change.txt', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project\\submodules\\linearizator' +
                                        ' && git add -A', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project\\submodules\\linearizator' +
                                        ' && git commit -m "test_pending_shortcut test"', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs --pending --verbose',
                                        shell=True).decode('latin-1'))
        else:  # on linux / os x
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project/submodules/linearizator' +
                                        ' && touch change.txt', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project/submodules/linearizator' +
                                        ' && git add -A', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project/submodules/linearizator' +
                                        ' && git commit -m "test_pending_shortcut test"', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs --pending --verbose',
                                        shell=True).decode('latin-1'))

    def test_in_branch_shortcut(self):
        if os.name == 'nt':  # on windows
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project\\submodules\\linearizator' +
                                        ' && git checkout develop', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '\\tmp\\git_submodules_test_project' + ' && pfs --in-branch develop --verbose',
                                        shell=True).decode('latin-1'))
        else:  # on linux / os x
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs -c "git checkout master"',
                                        shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project/submodules/linearizator' +
                                        ' && git checkout develop', shell=True).decode('utf-8'))
            print(self.sub.check_output('cd ' + os.path.dirname(os.path.abspath(__file__)) +
                                        '/tmp/git_submodules_test_project' + ' && pfs --not-in-branch develop --verbose',
                                        shell=True).decode('latin-1'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

