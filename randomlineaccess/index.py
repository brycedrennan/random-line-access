import math
import random
from pathlib import Path

from .utils import normalize_slice


def create_index(file_path, index_path, index_ratio, index_width):
    """

    Index format:
        1st byte: index_ratio
        2nd byte: index_width
        3rd byte: line_count
    """
    i = 0
    with file_path.open() as f:
        with index_path.open('wb') as idx:
            idx.write(index_ratio.to_bytes(1, byteorder='big'))
            idx.write(index_width.to_bytes(1, byteorder='big'))
            idx.write((0).to_bytes(32, byteorder='big'))  # holder for line_count that we'll write at the end
            idx.write((0).to_bytes(index_width, byteorder='big'))
            while f.readline():
                i += 1
                if (i % index_ratio) == 0:
                    pointer = f.tell()
                    b = pointer.to_bytes(index_width, byteorder='big')
                    idx.write(b)
            idx.seek(2)
            idx.write(i.to_bytes(32, byteorder='big'))


class IndexedOpen(object):
    """
    Indexed text file reader.

    Directly access a given line in a text file without iterating over the entire file.  This is similar to the linecache
    module that comes with python except linecache uses a non-persistent in-memory store.
    """

    def __init__(self, filepath, encoding=None, errors=None, newline=None, index_ratio=1, index_width=5):
        """
        Open a text file

        :param filepath:
        :param encoding:
        :param errors:
        :param newline:
        :param index_ratio:
        :param index_width:
        """
        self.filepath = Path(filepath)
        self.file = self.filepath.open(encoding=encoding, errors=errors, newline=newline)
        self.index = self.get_or_create_index(index_ratio, index_width)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __getitem__(self, slice_obj):
        """
        Supports slice operations on the file

        For example:

            with IndexedOpen(filename) as f:
                print f[6:-2]

        """
        start, stop, step = normalize_slice(slice_obj, self.index.line_count)
        if isinstance(slice_obj, slice):
            return [self._get_line(i) for i in range(start, stop, step)]
        elif isinstance(slice_obj, int):
            return self._get_line(start)

    def close(self):
        self.file.close()
        self.index.close()

    def get_or_create_index(self, index_ratio, index_width):
        """Return an open file-object to the index file"""
        if not self.index_path.exists():
            create_index(self.filepath, self.index_path, index_ratio=index_ratio, index_width=index_width)
        return IndexFile(str(self.index_path))

    @property
    def index_path(self):
        """the path to the index file"""
        return Path(str(self.filepath) + '.idx')

    def _get_line(self, line_no):
        line_pointer, lines_away_from_target = self.index.line_location(line_no)
        self.file.seek(line_pointer)
        line = self.file.readline()
        for _ in range(lines_away_from_target):
            line = self.file.readline()
        return line

    def random_line(self):
        return self[random.randrange(0, self.index.line_count)]


class IndexFile(object):
    def __init__(self, index_file_path):
        """
        Open a line-number index for a text file.
        """
        self.index_path = Path(index_file_path)
        self.header_length = 34
        self.index = self._open_index()

    def _open_index(self):
        index = self.index_path.open('rb')
        self.index_ratio = int.from_bytes(index.read(1), byteorder='big')
        self.index_width = int.from_bytes(index.read(1), byteorder='big')
        self.line_count = int.from_bytes(index.read(32), byteorder='big')
        return index

    def close(self):
        self.index.close()

    def line_location(self, line_no):
        index_line_no = math.floor(line_no / self.index_ratio)
        self.index.seek(index_line_no * self.index_width + self.header_length)
        main_file_pointer = self.index.read(self.index_width)
        main_file_pointer = int.from_bytes(main_file_pointer, byteorder='big')
        lines_away_from_target = line_no % self.index_ratio
        return main_file_pointer, lines_away_from_target
