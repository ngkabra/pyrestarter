# Needed only if you are running nosetests from local directory
# nosetests test_api - should work
import sys
from os.path import dirname, join
sys.path.append(dirname(dirname(dirname(__file__))))

import unittest
import psutil
import subprocess

class TestError(Exception):
    pass


class MultipleProcessesFound(TestError):
    pass


class Test(unittest.TestCase):
    def setUp(self):
        self.config_file = join(dirname(__file__), 'testconfig.cfg')
        self.verifiers = ('verifier1', 'verifier2', '13079')
        self.cmd = ['python',
                    join(dirname(dirname(__file__)), '__init__.py'),
                    '-c',
                    join(dirname(__file__), 'testconfig.py'),]

    def tearDown(self):
        self.killall()

    def killall(self):
        for verifier in self.verifiers:
            self.kill_process(verifier)

    def kill_process(self, verifier):
        for p in self.find_process(verifier, all=True):
            p.kill()

    def find_process(self, verifier, all=False):
        found_p = []
        for pid in psutil.get_pid_list():
            try:
                p = psutil.Process(pid)
            except psutil.error.NoSuchProcess:
                pass
            pcmd = ' '.join(p.cmdline)
            if verifier in pcmd:
                found_p.append(p)
        if all:
            return found_p
        elif found_p:
            if len(found_p) == 1:
                return found_p[0]
            else:
                print [(p.pid, p.cmdline) for p in found_p]
                raise MultipleProcessesFound(verifier)
        else:
            return None

    def assertProcess(self, verifier):
        self.assertTrue(self.find_process(verifier), msg=verifier)

    def assertNoProcess(self, verifier):
        self.assertFalse(self.find_process(verifier), msg=verifier)

    def assertAllProcesses(self):
        for verifier in self.verifiers:
            self.assertProcess(verifier)

    def assertNoProcesses(self):
        for verifier in self.verifiers:
            self.assertNoProcess(verifier)

    def test_start(self):
        self.assertNoProcesses()
        subprocess.call(self.cmd)
        self.assertAllProcesses()
        self.killall()
        self.assertNoProcesses()
        subprocess.call(self.cmd)
        self.assertAllProcesses()
        for verifier_to_kill in self.verifiers:
            self.kill_process(verifier_to_kill)
            for verifier in self.verifiers:
                if verifier == verifier_to_kill:
                    self.assertNoProcess(verifier)
                else:
                    self.assertProcess(verifier)
            subprocess.call(self.cmd)
            self.assertAllProcesses()



