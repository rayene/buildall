import tarfile

from buildall import Task, Path


class Decompress(Task):
    def __init__(self, decompressed):
        self._decompressed = decompressed

    def target(self):
        return Path(self._decompressed)

    def build(self, compressed):
        self.debug('Decompressing %s to %s' % (compressed,
                                               self._decompressed))
        with tarfile.open(str(compressed)) as f:
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(f, str(Path(self._decompressed).parent))
        assert Path(self._decompressed).exists()
        Path(self._decompressed).touch()
