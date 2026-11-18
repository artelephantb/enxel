from random import randint


soup = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_uid(length=10):
	final = 'e'
	for idx in range(length - 1):
		final += soup[randint(0, len(soup) - 1)]
	return final
