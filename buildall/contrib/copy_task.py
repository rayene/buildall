import shutil
from buildall import Task, Path

class CopyTask(Task):
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    def inputs(self):
        return Path(self._source),

    def targets(self):
        return Path(self._destination),

    def command(self):
        self.debug('Copying %s to %s' % (self._source,
                                              self._destination))
        shutil.copyfile(str(Path(self._source)), str(Path(self._destination)))
