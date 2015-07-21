from unittest import TestCase
from buildall import Task, Popen

class ExitTask(Task):
    def __init__(self, target_exit_value):
        self.target_exit_value = target_exit_value

    def target(self):
        return Popen('exit %d' % self.target_exit_value, shell=True)

    def build(self, *args):
        raise Exception('I have been called')


class TestPipelineWithPopen(TestCase):

    def test_exit_1(self):
        e = ExitTask(1)
        with self.assertRaisesRegex(Exception, 'I have been called'):
            e.make()

    def test_exit_0_0(self):
        e = ExitTask(0) << Popen('exit 0', shell=True)
        e.make()

    def test_exit_0_1(self):
        e = ExitTask(0) << Popen('exit 1', shell=True)
        with self.assertRaisesRegex(Exception, 'I have been called'):
            e.make()

    def test_exit_1_0(self):
        e = ExitTask(1) << Popen('exit 0', shell=True)
        with self.assertRaisesRegex(Exception, 'I have been called'):
            e.make()

    def test_exit_1_1(self):
        e = ExitTask(1) << Popen('exit 1', shell=True)
        with self.assertRaisesRegex(Exception, 'I have been called'):
            e.make()