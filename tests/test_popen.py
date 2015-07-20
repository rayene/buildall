from unittest import TestCase
from buildall import Task, Popen


class ExitTask(Task):
	def __init__(self, input_exit_value, target_exit_value):
		self.input_exit_value = input_exit_value
		self.target_exit_value = target_exit_value

	def inputs(self):
		return Popen('exit %d' % self.input_exit_value, shell=True),

	def targets(self):
		return Popen('exit %d' % self.target_exit_value, shell=True),

	def command(self):
		raise Exception('I have been called')


class TestPipelineWithPopen(TestCase):

	def test_exit_0_0(self):
		ExitTask(0, 0).make()

	def test_exit_0_1(self):
		with self.assertRaisesRegex(Exception, 'I have been called'):
			ExitTask(0, 1).make()

	def test_exit_1_0(self):
		with self.assertRaisesRegex(Exception, 'I have been called'):
			ExitTask(1, 0).make()

	def test_exit_1_1(self):
		with self.assertRaisesRegex(Exception, 'I have been called'):
			ExitTask(1, 1).make()