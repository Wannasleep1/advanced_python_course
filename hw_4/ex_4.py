def flat_generator(elem):
    if type(elem) != list:
        yield elem
    else:
        for item in elem:
            yield from flat_generator(item)


if __name__ == "__main__":
    nested_lst = [
        ['a', [['b'], 'c']],
        [[['d', 'e'], 'f', 'h'], [], [False]],
        [[1, [[2], None]]],
    ]
    for item in flat_generator(nested_lst):
        print(item)
    print([item for item in flat_generator(nested_lst)])