import urllib.request
import hashlib
from buildall import Task, BuildException, Path

class DownloadTask(Task):
    def __init__(self, url, destination, md5=None):
        self._url = url
        self._destination = destination
        self._md5 = md5

    def inputs(self):
        return []

    def targets(self):
        return Path(self._destination),

    def command(self):
        self.debug('Downloading %s to %s' % (self._url,
                                              self._destination))
        urllib.request.urlretrieve(self._url, self._destination)
        if not self._md5:
            return
        with open(self._destination, 'rb') as f:
            hasher = hashlib.md5()
            hasher.update(f.read())

        if self._md5 != hasher.hexdigest():
            raise BuildException('Download corrupt !')
