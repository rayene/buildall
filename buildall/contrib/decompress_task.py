from buildall import Task, BuildException, Path
import tarfile

class DecompressTask(Task):
    def __init__(self, compressed, decompressed):
        self._compressed = compressed
        self._decompressed = decompressed

    def inputs(self):
        return Path(self._compressed),

    def targets(self):
        return Path(self._decompressed),

    def command(self):
        self.debug('Decompressing %s to %s' % (self._compressed,
                                              self._decompressed))
        with tarfile.open(self._compressed) as f:
            f.extractall(str(Path(self._decompressed).parent))
        assert Path(self._decompressed).exists()
        Path(self._decompressed).touch()
