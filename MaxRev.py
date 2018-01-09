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


def pick(stock, comps, cur, temp, rev):
	print temp
	if not comps:
		return 0
	if stock < 0:
		c = temp.pop()
		return rev - price[c]
	elif stock == 0:
		return rev
	else:
		comps.remove(cur)
		for company in comps:
			prev = temp[:]
			temp.append(company)
			sel = pick(stock-quantity[company], comps[:], company, temp, rev+price[company])
			notsel = pick(stock, comps[:], company, prev, rev)
			if sel > notsel:
				rev = sel
			else:
				rev = notsel
		return rev

rev = 0

for c in companies:
	temp = [c]
	prev = []
	sel = pick(supply-quantity[c], companies[:], c, temp, price[c])
	notsel = pick(supply, companies[:], c, prev, 0)
	if sel > rev:
		rev = sel
		best = temp
	if notsel > rev:
		rev = notsel
		best = prev
print best