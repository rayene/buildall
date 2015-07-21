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

    def __init__(self, prog_file):
        self._prog_file = Path(prog_file)
        self.trigger_exception_if_buit = False

    def target(self):
        return self._prog_file

    def build(self, lib1_obj, lib2_obj, lib3_obj = None):
        if self.trigger_exception_if_buit:
            raise Exception('Sould not be rebuilt')
        #os.system('gcc lib1.o lib2.o -o myprogram')
        assert lib1_obj.exists()
        assert lib2_obj.exists()
        if lib3_obj:
            assert lib3_obj.exists()
        self._prog_file.touch()


class TestCompile(TestCase):
    def setUp(self):
        Path('lib1.c').touch()
        Path('lib2.c').touch()
        Path('lib3.c').touch()
        create_lib1 = CreateObjFile('lib1') << Path('lib1.c')
        create_lib2 = CreateObjFile('lib1') << Path('lib2.c')
        create_lib3 = CreateObjFile('lib3') << Path('lib3.c')
        self.create_prog1 = CreateProgram('myprogram') <<  create_lib1 + \
                                                           create_lib2
        self.create_prog2 = CreateProgram('myprogram') <<  create_lib1 + \
                                                           create_lib2 + \
                                                           create_lib3


    def tearDown(self):
        try:
            for p in Path('.').glob('lib*'):
                p.unlink()
            Path('myprogram').unlink()
        except:
            pass

    def test_compile_from_scratch(self):
        self.create_prog1.make()
        self.assertTrue(Path('myprogram').exists())

    def test_recompile_from_scratch(self):
        self.create_prog1.make()
        self.assertTrue(Path('myprogram').exists())
        time.sleep(1.1)
        self.create_prog1.trigger_exception_if_buit = True
        self.create_prog1.make()


    def test_compile_with_three_dependencies(self):
        self.create_prog2.make()
        self.assertTrue(Path('myprogram').exists())
