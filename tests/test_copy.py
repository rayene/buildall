from unittest import TestCase
from buildall.contrib.copy_task import CopyTask, Path
import tarfile

class TestCopyTask(TestCase):

    def test_copy_task(self):
        Path('a').touch()
        cp = CopyTask('b') << Path('a')
        cp.make()
        self.assertTrue(Path('b').exists())


    def tearDown(self):
        Path('a').unlink()
        Path('b').unlink()
