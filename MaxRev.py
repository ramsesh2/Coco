import argparse
import csv

#grab the supply of product available

parser = argparse.ArgumentParser(description='Choose which orders to fill.')
parser.add_argument('supply', nargs=1, type=int,
				help='Total supply of product available')

arg = parser.parse_args()
#print arg.supply[0]
supply = arg.supply[0]


quantity = {}
price = {}
unit_price = {}
companies = []
with open('Orders.csv', 'r') as orders:
	reader = csv.reader(orders, delimiter=',')
	for row in reader:
		quantity[row[0]] = int(row[1])
		unit_price[row[0]] = float(row[2])/int(row[1])
		price[row[0]] = int(row[2])
		companies.append(row[0])

best = []


def pick(stock, comps):
	print stock
	if not comps:
		return 0
	if stock == 0:
		return 0
	last = comps.pop()

	if stock - quantity[last] < 0:
		return pick(stock, comps)

	else:
		sel = price[last] + pick(stock-quantity[last], comps)
		notsel = pick(stock, comps)
		if(sel > notsel):
			best.append(last)
			return sel
		else:
			return notsel

print pick(supply, companies)
print best