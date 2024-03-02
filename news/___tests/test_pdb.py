import pdb


# def integers_counter(data):
#     integers_found = 0
#     for item in data:
#         if not isinstance(item, bool) and isinstance(item, int):
#             integers_found += 1
#     return integers_found


# def test_counter():
#     data = [False, 1.0, "some_string", 3, True, 1, [], False]
#     integers = integers_counter(data)
#     assert integers == 2


def transform_list(x):
    x.append(1)
    x.extend([2, 3])
    return x


def test_list():
    a = []
    a = transform_list(a)
    # pdb.set_trace()
    a = [4] + a
    assert a == [1, 2, 3, 4]
