import aiger as A
import aiger_bv as BV
import aiger_coins as C
import aiger_gridworld as GW
import aiger_ptltl as LTL
import funcy as fn
import matplotlib.pyplot as plt
import seaborn as sns
from bidict import bidict
from IPython.display import HTML as html_print
from IPython.display import *

NORTH = '↑'
SOUTH = '↓'
EAST = '→'
WEST = '←'


ACTIONS = bidict({
	#      y   x
	'←': 0b00_01,
	'→': 0b00_10,
	'↓': 0b01_00,
	'↑': 0b10_00,
})


ACTIONS_C = bidict({'←': 0b00, '↑': 0b01, '→': 0b10, '↓': 0b11})
COMPRESSION_MAPPING = {
	ACTIONS_C['→']: ACTIONS['→'],
	ACTIONS_C['←']: ACTIONS['←'],
	ACTIONS_C['↑']: ACTIONS['↑'],
	ACTIONS_C['↓']: ACTIONS['↓'],
}

COLOR_ALIAS = {
	'yellow': '#ffff8c', 'brown': '#ffb081',
	'red': '#ff5454', 'blue': '#9595ff'
	}

def mask_test(xmask, ymask, X, Y):
	return ((X & xmask) !=0) & ((Y & ymask) != 0)


def encode_state(x, y):
	x, y = [BV.encode_int(8, 1 << (v - 1), signed=False) for v in (x, y)]
	return {'x': tuple(x), 'y': tuple(y)}

def create_sensor(aps):
	sensor = BV.aig2aigbv(A.empty())
	for name, ap in aps.items():
		sensor |= ap.with_output(name).aigbv
	return sensor

def tile(color='black'):
	color = COLOR_ALIAS.get(color, color)
	s = '&nbsp;'*4
	return f"<text style='border: solid 1px;background-color:{color}'>{s}</text>"


def ap_at_state(x, y, SENSOR, in_ascii=False):
	"""Use sensor to create colored tile."""
	state = encode_state(x, y)
	obs = SENSOR(state)[0]   # <----------   

	for k in COLOR_ALIAS.keys():
		if obs[k][0]:
			return tile(k)
	return tile('white')

def print_map(sensor):
	"""Scan the board row by row and print colored tiles."""
	order = range(1, 9)
	for y in order:
		chars = (ap_at_state(x, y, sensor, in_ascii=True) for x in order)
		obj = html_print('&nbsp;'.join(chars))
		display_html(obj)
		

def main():
	print("START")
	X = BV.atom(8, 'x', signed=False)
	Y = BV.atom(8, 'y', signed=False)
	APS = {       #            x-axis       y-axis
		'yellow': mask_test(0b1000_0001, 0b1000_0001, X, Y),
		'blue':   mask_test(0b0001_1000, 0b0011100, X, Y),
		'brown':   mask_test(0b0011_1100, 0b1000_0001, X, Y),
		'red':    mask_test(0b1000_0001, 0b0100_1100, X, Y) \
			| mask_test(0b0100_0010, 0b1100_1100, X, Y),
	}

	SENSOR = create_sensor(APS)

	print_map(SENSOR)
	print("SUCCESS")
	# for i, trc in enumerate(set(TRACES)):
	# 	print()
	# 	print(f'trace {i}')
	# 	print_trc(trc)

	# infer()


if __name__ == '__main__':
	main()
