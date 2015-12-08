def dot_product(x, y):
    assert len(x) == len(y)
    return sum([a * b for (a, b) in zip(x, y)])