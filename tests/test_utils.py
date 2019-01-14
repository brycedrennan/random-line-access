import pytest

from randomlineaccess.utils import normalize_slice


def test_slices():
    class SliceTester:
        def __getitem__(self, item):
            return normalize_slice(item, 100)

    s = SliceTester()

    assert s[5] == (5, 6, 1)
    assert s[-1] == (99, 100, 1)
    assert s[:] == (0, 100, 1)
    assert s[0:] == (0, 100, 1)
    assert s[1:] == (1, 100, 1)
    assert s[-4:] == (96, 100, 1)
    assert s[-4:-2] == (96, 98, 1)
    assert s[5:99] == (5, 99, 1)
    assert s[5:-1] == (5, 99, 1)

    with pytest.raises(IndexError):
        assert s[100]

    with pytest.raises(IndexError):
        assert s[-101]

    with pytest.raises(TypeError):
        assert s["hello"]
