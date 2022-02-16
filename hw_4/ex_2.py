def flat_generator(nested_list):
	for iterable in nested_list:
		for item in iterable:
			yield item


if __name__ == '__main__':
	nested_lst = [
		['a', 'b', 'c'],
		['d', 'e', 'f'],
		[1, 2, None],
	]
	for elem in flat_generator(nested_lst):
		print(elem)
		