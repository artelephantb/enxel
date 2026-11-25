from random import randint


SOUP_ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
SOUP_ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SOUP_NUMBERS = '0123456789'

SOUP = SOUP_ALPHA_LOWER + SOUP_ALPHA_UPPER + SOUP_NUMBERS


def generate_uid(length=10):
	final = 'e'
	for idx in range(length - 1):
		final += SOUP[randint(0, len(SOUP) - 1)]
	return final

def generate_uid_numbers(length=10):
	final = ''
	for idx in range(length - 1):
		final += SOUP_NUMBERS[randint(0, len(SOUP_NUMBERS) - 1)]
	return final
