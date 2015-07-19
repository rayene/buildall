from pathlib import PosixPath as PythonPathClass
from subprocess import Popen as PythonPopenClass

END_OF_TIME = 9999999999999999999 # TODO: find a better value

class BaseTask:

	_indent_level = 0
	silent = False

	def __str__(self):
		return self.__class__.__name__

	def inputs(self):
		return []

	def command(self):
		raise NotImplementedError('You should implement your own command() method')

	def targets(self):
		return []


	def debug(self, msg):
		indent = self._indent_level * '\t'
		if not self.silent:
			print(indent + '<%s> ' % self + msg)

	def set_indent_level(self, level):
		self._indent_level = level

	def is_up_to_date(self, dependencies_modification_time):
		if self.modification_time < dependencies_modification_time:
			self.debug('Target unsatisfied. Will trigger the build !')
			return False
		self.debug('Target is up-to-date')
		return True




class Task(BaseTask):
	@property
	def modification_time(self):
		mod_times = [target.modification_time for target in self.targets()]
		if mod_times == []:
			return 0
		return max(mod_times)


	def make(self):
		self.debug('')
		newest_dependency_mod_time = 0
		for input_ in self.inputs():
			input_.set_indent_level(self._indent_level + 1)
			dependency_mod_time = input_.make()
			newest_dependency_mod_time = max(newest_dependency_mod_time, dependency_mod_time)

		if newest_dependency_mod_time == END_OF_TIME:
			#self.debug('At least, one of the dependencies triggered the build !')
			self.command()
			self.debug('Regeneration succeeded !')
			return END_OF_TIME

		#self.debug('Cannot make a decision based solely on dependencies. Will check targets !')
		for target in self.targets():
			target.set_indent_level(self._indent_level + 1)
			if not target.is_up_to_date(newest_dependency_mod_time):
				self.command()
				self.debug('Regeneration succeeded !')
				return END_OF_TIME
		return self.modification_time

class Path(PythonPathClass, BaseTask):
	@property
	def modification_time(self):
		if self.exists():
			mod_ts = self.stat().st_mtime_ns
			return mod_ts
		return -1

	def make(self):
		mod_ts = self.stat().st_mtime_ns
		self.debug('Dependency file exists and its date is %d' % mod_ts)
		return mod_ts


class Popen(PythonPopenClass, BaseTask):
	def __str__(self):
		return self.__class__.__name__ + ' - ' + str(self.args)

	@property
	def modification_time(self):
		if self.wait() == 0:
			return END_OF_TIME
		return -1

	def make(self):
		if self.wait() == 0:
			self.debug('Dependency command exited with return code 0 => satisfied')
			return 0
		self.debug('Dependency command exited with return code !=0 => Will trigger ancestors build methods')
		return END_OF_TIME


class BuildException(Exception):
	pass