from unittest import TestCase
from buildall.contrib.download_task import DownloadTask, Path, BuildException

class TestDownloadTask(TestCase):
    def download_jquery(self, md5):
        d = DownloadTask(
            url='https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js',
            destination='jquery.min.js',
            md5=md5
        )
        d.make()
        self.assertTrue(Path('jquery.min.js').exists())
        Path('jquery.min.js').unlink()


    def test_download_task_without_md5(self):
        self.download_jquery(None)

    def test_download_task_with_md5(self):
        self.download_jquery('32015dd42e9582a80a84736f5d9a44d7')

    def test_download_with_wrong_md5(self):
        with self.assertRaisesRegex(BuildException, 'Download corrupt'):
            self.download_jquery('this is a wrong md5')