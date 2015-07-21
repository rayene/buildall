from unittest import TestCase
from buildall import Task, Path
import time


class CreateObjFile(Task):
    def __init__(self, filename):
        self.filename = filename

    def target(self):
        return Path(self.filename + '.o')

    def build(self, c_file):
        #os.system('gcc -c %s.o -o %s.o'%c_file)
        assert c_file.exists()
        Path(self.filename + '.o').touch()


class CreateProgram(Task):
    trigger_exception_if_buit = False
    def __init__(self, prog_file):
        self._prog_file = Path(prog_file)

    def target(self):
        return self._prog_file

    def build(self, lib1_obj, lib2_obj):
        if self.trigger_exception_if_buit:
            raise Exception('Sould not be rebuilt')
        #os.system('gcc lib1.o lib2.o -o myprogram')
        assert lib1_obj.exists()
        assert lib2_obj.exists()
        self._prog_file.touch()


class TestCompile(TestCase):
    def setUp(self):
        Path('lib1.c').touch()
        Path('lib1.h').touch()
        Path('lib2.c').touch()
        Path('lib2.h').touch()
        create_lib1 = CreateObjFile('lib1') << Path('lib1.c')
        create_lib2 = CreateObjFile('lib1') << Path('lib2.c')
        self.create_prog = CreateProgram('myprogram') <<  create_lib1 + create_lib2

    def tearDown(self):
        try:
            for p in Path('.').glob('lib*'):
                p.unlink()
            Path('myprogram').unlink()
        except:
            pass

    def test_compile_from_scratch(self):
        self.create_prog.make()
        self.assertTrue(Path('myprogram').exists())

    def test_recompile_from_scratch(self):
        self.create_prog.make()
        self.assertTrue(Path('myprogram').exists())
        time.sleep(1.1)
        CreateProgram.trigger_exception_if_buit = True
        self.create_prog.make()