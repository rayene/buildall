import datetime
from pathlib import PosixPath as PythonPathClass
from subprocess import Popen as PythonPopenClass

# TODO: find a better value
END_OF_TIME = datetime.datetime(2100, 1, 1)
BEGINNING_OF_TIME = datetime.datetime(1970, 1, 1)


class BaseTask:
    _indent_level = 0
    silent = False
    _child_tasks = []

    def __str__(self):
        return self.__class__.__name__

    def build(self, *args):
        raise NotImplementedError('You should implement your own build()')

    def target(self):
        return None

    def debug(self, msg):
        indent = self._indent_level * '\t'
        if not self.silent:
            print(indent + '<%s> ' % self + msg)

    def set_indent_level(self, level):
        self._indent_level = level

    def is_up_to_date(self, dependencies_modification_time):
        if self.modification_time < dependencies_modification_time:
            self.debug('Target unsatisfied (%s). Will trigger the build !'
                       % self.modification_time)
            return False
        self.debug('Target is up-to-date')
        return True


class Task(BaseTask):
    @property
    def modification_time(self):
        mod_times = [target.modification_time for target in [self.target()] if
                     target is not None]
        if not mod_times:
            return BEGINNING_OF_TIME
        return max(mod_times)

    def make(self):
        self.debug('')
        newest_dependency_mod_time = BEGINNING_OF_TIME
        build_params = []
        for child in self._child_tasks:
            child.set_indent_level(self._indent_level + 1)
            dependency_mod_time = child.make()
            newest_dependency_mod_time = max(newest_dependency_mod_time,
                                             dependency_mod_time)
            build_params.append(child.target())

        if newest_dependency_mod_time == END_OF_TIME:
            # self.debug('At least, one of the dependencies triggered the
            # build')
            self.build(*build_params)
            self.debug('Regeneration succeeded !')
            return END_OF_TIME

        # self.debug('Cannot decide based on dependencies. Checking targets')
        for target in [self.target()]:
            if target is None:
                continue
            target.set_indent_level(self._indent_level + 1)
            if not target.is_up_to_date(newest_dependency_mod_time):
                self.build(*build_params)
                self.debug('Regeneration succeeded !')
                return END_OF_TIME
        self.debug('Nothing to do !')
        return self.modification_time

    def __add__(self, other):
        return TargetList() + self + other

    def __lshift__(self, other):
        # 'other' can be a task or a list of tasks
        try:
            iter(other)
            self._child_tasks = other
        except TypeError:
            self._child_tasks = [other]
        return self


class TargetList(list):
    def __add__(self, other):
        if isinstance(other, BaseTask):
            self.append(other)
        else:
            super().__add__(other)
        return self


class Path(PythonPathClass, BaseTask):
    def target(self):
        return self

    @property
    def modification_time(self):
        if self.exists():
            mod_ts = self.stat().st_mtime_ns
            return datetime.datetime.fromtimestamp(mod_ts / 1000000000)
        return datetime.datetime(1969, 12, 31)

    def make(self):
        mod_ts = self.stat().st_mtime_ns
        mod_dt = datetime.datetime.fromtimestamp(mod_ts / 1000000000)
        self.debug('Dependency file exists and its date is %s' % mod_dt)
        return mod_dt


class Popen(PythonPopenClass, BaseTask):
    def target(self):
        return self

    def __str__(self):
        return self.__class__.__name__ + ' - ' + str(self.args)

    @property
    def modification_time(self):
        if self.wait() == 0:
            return END_OF_TIME
        return datetime.datetime(1969, 12, 31)

    def make(self):
        if self.wait() == 0:
            self.debug('Dependency build exited with return code 0 '
                       '=> satisfied')
            return BEGINNING_OF_TIME
        self.debug('Dependency build exited with return code !=0 '
                   '=> Will trigger ancestors build methods')
        return END_OF_TIME


class BuildException(Exception):
    pass