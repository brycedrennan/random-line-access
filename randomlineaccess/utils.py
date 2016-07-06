def normalize_slice(slice_obj, length):
    """
    Given a slice object, return appropriate values for use in the range function

    :param slice_obj: The slice object or integer provided in the `[]` notation
    :param length: For negative indexing we need to know the max length of the object.
    """
    if isinstance(slice_obj, slice):
        start, stop, step = slice_obj.start, slice_obj.stop, slice_obj.step
        if start is None:
            start = 0

        if stop is None:
            stop = length

        if step is None:
            step = 1

        if start < 0:
            start += length

        if stop < 0:
            stop += length
    elif isinstance(slice_obj, int):
        start = slice_obj
        if start < 0:
            start += length
        stop = start + 1
        step = 1
    else:
        raise TypeError

    if (0 <= start <= length) and (0 <= stop <= length):
        return start, stop, step

    raise IndexError
