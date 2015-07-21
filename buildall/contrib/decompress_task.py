from buildall import Task, BuildException, Path
import tarfile

class DecompressTask(Task):
    def __init__(self, decompressed):
        self._decompressed = decompressed

    def target(self):
        return Path(self._decompressed)

    def build(self, compressed):
        self.debug('Decompressing %s to %s' % (compressed,
                                              self._decompressed))
        with tarfile.open(str(compressed)) as f:
            f.extractall(str(Path(self._decompressed).parent))
        assert Path(self._decompressed).exists()
        Path(self._decompressed).touch()
