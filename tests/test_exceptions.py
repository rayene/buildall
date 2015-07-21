from unittest import TestCase
from buildall import Task, Popen, BuildException


class TestPipelineExceptions(TestCase):
    def test_command_not_implemented(self):
        class TaskA(Task):
            pass

        t = TaskA() << Popen('exit 1', shell=True)
        with self.assertRaisesRegex(NotImplementedError,
                                                'implement your own build'):
            t.make()

    def test_empty_targets_executed(self):
        class EmptyTargets(Task):
            def build(self, *args):
                raise BuildException('I have been called')

        t = EmptyTargets() << Popen('exit 1', shell=True)
        with self.assertRaisesRegex(BuildException, 'I have been called'):
            t.make()


    def test_empty_targets_not_executed(self):
        class EmptyTargets(Task):
            def build(self, *args):
                raise Exception('If called, the test fails')  # pragma: no cover

        t = EmptyTargets() << Popen('exit 0', shell=True)
        t.make()