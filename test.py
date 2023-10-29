#! /bin/python3
import time

a = 1103515245
b = 12345
m = 1 << 31
last_n = round(time.time() * 1000)

def rnd():
	global last_n
	last_n = ((a * last_n) + b) % m
	return last_n

def main():
	size = 100000000
	v = [0, 0, 0, 0, 0, 0]
	for i in range(1, size):
		idx = rnd() % 6
		v[idx] += 1

	for i in v:
		print(100 * i / size)


if __name__ == "__main__":
	main()
