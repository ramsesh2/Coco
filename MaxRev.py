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
python MaxRev.py [Supply of product available]

The customer order amounts and prices MUST reside in a file called
Orders.csv, each column delimited by a comma
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
companies = []
with open('Orders.csv', 'r') as orders:
	reader = csv.reader(orders, delimiter=',')
	for row in reader:
		quantity[row[0]] = int(row[1])
		unit_price[row[0]] = float(row[2])/int(row[1])
		price[row[0]] = int(row[2])
		companies.append(row[0])

best = []

#dynamic programming recursive function
def pick(stock, comps):
#	print stock

#if there are no more companies to look at or if there is no more supply
	if not comps:
		return 0
	if stock == 0:
		return 0

#pop the last element in the list of companies
	last = comps.pop()

#if there is not enough stock to fill the order, move on to the next one
	if stock - quantity[last] < 0:
		return pick(stock, comps)

#either choose the company or don't, build a tree of each of the possible combinations of companies
#whose orders will fit. Choose the path with the highest revenue in the end.
	else:
		sel = price[last] + pick(stock-quantity[last], comps)
		notsel = pick(stock, comps)
		if(sel > notsel):
			best.append(last)
			return sel
		else:
			return notsel

rev = pick(supply, companies)
#print best

print 'Should complete the following orders:'
quant = 0
for s in best:
	print 'Company: ', s, '   Amount: ', quantity[s],'   Price: ', price[s]
	quant += quantity[s]
print 'Total Quantity: ', quant, 'Total Revenue: ', rev