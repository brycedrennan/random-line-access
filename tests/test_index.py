import os
import tempfile

from randomlineaccess.index import IndexedOpen


def test_random_line():
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    for i in range(5):
        f.write('%i\n' % i)
    f.close()

    with IndexedOpen(f.name) as indexed_f:
        pw = ''.join(indexed_f.random_line().strip() for _ in range(200))

    # selected from all possible values
    assert len(set(pw)) == 5


def test_indexed_read_write():
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    written_to_file = []
    for i in range(100):
        f.write('%i\n' % i)
        written_to_file.append(str(i) + '\n')
    f.close()

    tmp_name = f.name

    # did we create the temporary file properly?
    with open(tmp_name) as f:
        assert list(f) == written_to_file

    # does the indexed access work?
    with IndexedOpen(f.name) as f:
        for i in range(10):
            assert str(i) == f[i].strip()

        assert f[5] == written_to_file[5]
        assert f[99] == written_to_file[99]
        assert f[-100] == written_to_file[-100]
        assert f[:] == written_to_file[:]
        assert f[0:] == written_to_file[0:]
        assert f[1:] == written_to_file[1:]
        assert f[-4:] == written_to_file[-4:]
        assert f[-4:-2] == written_to_file[-4:-2]
        assert f[5:99] == written_to_file[5:99]
        assert f[5:-1] == written_to_file[5:-1]

    os.remove(tmp_name)


def test_index_compression():
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    written_to_file = []
    for i in range(100):
        f.write('%i\n' % i)
        written_to_file.append(str(i) + '\n')
    f.close()

    tmp_name = f.name

    # did we create the temporary file properly?
    with open(tmp_name) as f:
        assert list(f) == written_to_file

    # does the indexed access work?
    with IndexedOpen(f.name, index_ratio=10) as f:
        for i in range(10):
            assert str(i) == f[i].strip()

        assert f[5] == written_to_file[5]
        assert f[99] == written_to_file[99]
        assert f[-100] == written_to_file[-100]
        assert f[:] == written_to_file[:]
        assert f[0:] == written_to_file[0:]
        assert f[1:] == written_to_file[1:]
        assert f[-4:] == written_to_file[-4:]
        assert f[-4:-2] == written_to_file[-4:-2]
        assert f[5:99] == written_to_file[5:99]
        assert f[5:-1] == written_to_file[5:-1]

    os.remove(tmp_name)
