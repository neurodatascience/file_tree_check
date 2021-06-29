import shutil
from pathlib import Path
import os


class FileChecker:
    """
    Will handle all checks done on individual files.
    Size is in bytes.
    """

    def __init__(self, min_size=50, min_permissions=(4, 4, 0)):
        self.min_size = min_size
        self.permissions = min_permissions

    def check_size(self, path):
        return path.stat().st_size > self.min_size

    def check_permissions(self, path):
        perm = list(path.st_mode & 0o777)
        if len(perm) == 3:
            return perm[0] >= self.permissions[0] & perm[1] >= self.permissions[1] & perm[2] >= self.permissions[2]
            # there's probably a better way to compare
        else:
            return None