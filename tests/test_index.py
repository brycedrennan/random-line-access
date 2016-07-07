import os
import tempfile

from randomlineaccess.index import IndexedOpen


def create_num_file(size):
    text_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    num_list = []
    for i in range(size):
        text_file.write('%i\n' % i)
        num_list.append(str(i) + '\n')
    text_file.close()

    # did we create the temporary file properly?
    with open(text_file.name) as tmpf:
        assert list(tmpf) == num_list

    return text_file.name, num_list


def test_random_line():
    text_file_name, num_list = create_num_file(5)

    with IndexedOpen(text_file_name) as indexed_f:
        pw = ''.join(indexed_f.random_line().strip() for _ in range(200))

    # selected from all possible values
    assert len(set(pw)) == 5


def test_indexed_read_write():
    text_file_name, num_list = create_num_file(100)

    # ensure behaves just like a real list would
    with IndexedOpen(text_file_name) as f:
        for i in range(10):
            assert str(i) == f[i].strip()

        assert f[5] == num_list[5]
        assert f[99] == num_list[99]
        assert f[-100] == num_list[-100]
        assert f[:] == num_list[:]
        assert f[0:] == num_list[0:]
        assert f[1:] == num_list[1:]
        assert f[-4:] == num_list[-4:]
        assert f[-4:-2] == num_list[-4:-2]
        assert f[5:99] == num_list[5:99]
        assert f[5:-1] == num_list[5:-1]
        assert f[5:10:2] == num_list[5:10:2]
        print(f.index.index_file.name)
    os.remove(text_file_name)


def test_index_updates():
    """Ensure index rebuilds if file is modified"""
    text_file_name, num_list = create_num_file(100)
    with IndexedOpen(text_file_name) as f:
        first_index_updated_time = f.index.index_path.stat().st_mtime

    # no changes, not modified
    with IndexedOpen(text_file_name) as f:
        assert first_index_updated_time == f.index.index_path.stat().st_mtime

    # change text file
    with open(text_file_name, 'w') as text_file:
        for i in range(10):
            text_file.write('%i\n' % i)

    # modified time on index changes to match modified file
    with IndexedOpen(text_file_name) as f:
        assert first_index_updated_time != f.index.index_path.stat().st_mtime


def test_index_compression():
    text_file_name, num_list = create_num_file(100)
    # does the indexed access work?
    with IndexedOpen(text_file_name, index_ratio=10) as f:
        for i in range(10):
            assert str(i) == f[i].strip()

        assert f[5] == num_list[5]
        assert f[99] == num_list[99]
        assert f[-100] == num_list[-100]
        assert f[:] == num_list[:]
        assert f[0:] == num_list[0:]
        assert f[1:] == num_list[1:]
        assert f[-4:] == num_list[-4:]
        assert f[-4:-2] == num_list[-4:-2]
        assert f[5:99] == num_list[5:99]
        assert f[5:-1] == num_list[5:-1]
        assert f[5:10:2] == num_list[5:10:2]

    os.remove(text_file_name)
