from unittest import TestCase
from buildall.contrib.copy import Copy, Path
import tarfile

class TestCopy(TestCase):

    def test_copy_task(self):
        Path('a').touch()
        cp = Copy('b') << Path('a')
        cp.make()
        self.assertTrue(Path('b').exists())


    def tearDown(self):
        Path('a').unlink()
        Path('b').unlink()
