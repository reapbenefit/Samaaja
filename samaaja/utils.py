from math import log, floor

def human_format(number):
	units = ['', 'K', 'M', 'G', 'T', 'P']
	k = 1000.0
	magnitude = int(floor(log(number, k)))
	return '%.2f%s' % (number / k**magnitude, units[magnitude])