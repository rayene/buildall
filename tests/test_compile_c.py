from unittest import TestCase
from buildall import Task, Path
import time


class CreateObjFile(Task):
	def __init__(self, filename):
		self.filename = filename

	def inputs(self):
		return Path(self.filename + '.c'), Path(self.filename + '.h')

	def targets(self):
		return Path(self.filename + '.o'),

	def command(self):
		#os.system('gcc -c %s.o -o %s.o'%self.filename)
		Path(self.filename + '.o').touch()

class CreateProgram(Task):
	def inputs(self):
		return CreateObjFile('lib1'), CreateObjFile('lib2')

	def targets(self):
		return Path('myprogram'),

	def command(self):
		#os.system('gcc lib1.o lib2.o -o myprogram')
		Path('myprogram').touch()


class TestCompile(TestCase):
	def setUp(self):
		Path('lib1.c').touch()
		Path('lib1.h').touch()
		Path('lib2.c').touch()
		Path('lib2.h').touch()

	def tearDown(self):
		for p in Path('.').glob('lib*'):
			p.unlink()
		Path('myprogram').unlink()

	def test_compile_from_scratch(self):
		CreateProgram().make()

	def test_recompile_from_scratch(self):
		CreateProgram().make()
		time.sleep(1)
		CreateProgram().make()