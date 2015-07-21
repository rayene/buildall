import shutil

from buildall import Task, Path


class Copy(Task):
    def __init__(self, destination):
        self._destination = Path(destination)

    def target(self):
        return self._destination

    def build(self, source):
        assert source.exists()
        self.debug('Copying %s to %s' % (source,
                                         self._destination))
        shutil.copyfile(str(source), str(self._destination))
