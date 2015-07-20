from unittest import TestCase
from buildall.contrib.decompress_task import DecompressTask, Path
import tarfile

class TestDownloadTask(TestCase):
    def test_download_task(self):
        Path('a').touch()
        with tarfile.open('a.tar.gz', 'w') as t:
            t.add('a')
        Path('a').unlink()
        d = DecompressTask(compressed = 'a.tar.gz', decompressed = 'a')
        d.make()
        self.assertTrue(Path('a').exists())
        Path('a.tar.gz').unlink()
        Path('a').unlink()
