from unittest import TestCase
from buildall.contrib.decompress_task import DecompressTask, Path
import tarfile

class TestDecompressTask(TestCase):
    def test_decompress_task(self):
        Path('a').touch()
        with tarfile.open('a.tar.gz', 'w') as t:
            t.add('a')
        Path('a').unlink()
        d = DecompressTask('a') << Path('a.tar.gz')
        d.make()
        self.assertTrue(Path('a').exists())

    def tearDown(self):
        try:
            Path('a.tar.gz').unlink()
            Path('a').unlink()
        except FileNotFoundError:
            pass
