from unittest import TestCase
from buildall import Task, Popen, BuildException


class TestPipelineExceptions(TestCase):
	def test_command_not_implemented(self):
		class TaskA(Task):
			def inputs(self):
				return Popen('exit 1', shell=True),

		with self.assertRaisesRegex(NotImplementedError,
												'implement your own command'):
			TaskA().make()

	def test_empty_targets_executed(self):
		class EmptyTargets(Task):
			def inputs(self):
				return Popen('exit 1', shell=True),

			def command(self):
				raise BuildException('I have been called')

		with self.assertRaisesRegex(BuildException, 'I have been called'):
			EmptyTargets().make()

	def test_empty_targets_not_executed(self):
		class EmptyTargets(Task):
			def inputs(self):
				return Popen('exit 0', shell=True),

			def command(self):
				raise Exception('If called, the test fails')  # pragma: no cover

		EmptyTargets().make()