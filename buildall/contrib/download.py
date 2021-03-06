import urllib.request
import hashlib

from buildall import Task, BuildException, Path


class Download(Task):
    def __init__(self, url, destination, md5=None):
        self._url = url
        self._destination = destination
        self._md5 = md5

    def target(self):
        return Path(self._destination)

    def build(self):
        self.debug('Downloading %s to %s' % (self._url,
                                             self._destination))
        urllib.request.urlretrieve(self._url, self._destination)
        if not self._md5:
            return
        with open(self._destination, 'rb') as f:
            hasher = hashlib.md5()
            hasher.update(f.read())
        md5 = hasher.hexdigest()
        if self._md5 != md5:
            raise BuildException('Download corrupt ! '
                                 'Expected md5="%s", found="%s"' % (
                                 self._md5, md5))
