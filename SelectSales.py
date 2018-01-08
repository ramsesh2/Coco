'''
To select the companies to sell to in order to achieve maximum revenue

Assumptions made:

1) Orders can only be completed in full. If a company requests 5 items at a 
	price, then you can only sell them exactly 5.
2) The price given is the price the company is willing to pay for the 
	total quantity given, NOT the per unity price.
3) I am sticking to built in python data structures (dictionaries and lists, 
	but a better approach would be a dataframe or database to keep the data
	tabular. I did not use those to keep the solution simple and portable.

usage:
python SelectSales.py [Supply of product available]
'''

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
with open('Orders.csv', 'r') as orders:
	reader = csv.reader(orders, delimiter=',')
	for row in reader:
		quantity[row[0]] = int(row[1])
		unit_price[row[0]] = float(row[2])/int(row[1])
		price[row[0]] = int(row[2])

print quantity
print price
print unit_price
priceAscending = sorted(price, key=lambda entry: unit_price[entry])
print priceAscending
sales = {}
revenue = 0
while supply > 0:
	if not priceAscending:
		break
	company = priceAscending.pop()
	print supply
	print company
	if supply - quantity[company] < 0:
		continue
		'''
		sales[company] = supply
		supply -= supply
		'''
	else:
		sales[company] = quantity[company]
		supply -= quantity[company]
		revenue += price[company]

print sales
print revenue