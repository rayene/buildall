from unittest import TestCase
import tarfile

from buildall.contrib.decompress import Decompress, Path


class TestDecompress(TestCase):
    def test_decompress_task(self):
        Path('a').touch()
        with tarfile.open('a.tar.gz', 'w') as t:
            t.add('a')
        Path('a').unlink()
        d = Decompress('a') << Path('a.tar.gz')
        d.make()
        self.assertTrue(Path('a').exists())

    def tearDown(self):
        try:
            Path('a.tar.gz').unlink()
            Path('a').unlink()
        except FileNotFoundError:
            pass
