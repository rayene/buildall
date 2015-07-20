from unittest import TestCase
from buildall.contrib.download_task import DownloadTask, Path

class TestDownloadTask(TestCase):
    def test_download_task(self):
        d = DownloadTask(
            url='https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js',
            destination='jquery.min.js',
            md5=None
        )
        d.make()
        self.assertTrue(Path('jquery.min.js').exists())
        Path('jquery.min.js').unlink()