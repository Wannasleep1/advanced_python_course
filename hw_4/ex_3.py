from typing import List, Any


class FlatIterator:

    def __init__(self, nested_list):
        self.__check_type(nested_list)
        self.__nested_list: list = nested_list

    @staticmethod
    def __check_type(value):
        if type(value) != list:
            raise TypeError("'value' attribute must be list type.")

    @property
    def nested_list(self):
        return self.__nested_list

    @nested_list.setter
    def nested_list(self, value):
        self.__check_type(value)
        self.__nested_list = value

    @nested_list.deleter
    def nested_list(self):
        self.__nested_list = []

    @classmethod
    def __unnest_recursively(cls, elem) -> list:
        if type(elem) != list:
            yield elem
        else:
            for item in elem:
                yield from cls.__unnest_recursively(item)

    def __iter__(self):
        return self.__unnest_recursively(self.__nested_list)


if __name__ == "__main__":
    nested_lst = [
        ['a', [['b'], 'c']],
        [[['d', 'e'], 'f', 'h'], [], [False]],
        [[1, [[2], None]]],
    ]
    flat_iter = FlatIterator(nested_lst)
    for item in flat_iter:
        print(item)
    flat_list = [item for item in FlatIterator(nested_lst)]
    print(flat_list)