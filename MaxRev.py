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

best = [[0 for x in range(supply + 1)] for y in range(len(companies) + 1)]
keep = [[0 for x in range(supply + 1)] for y in range(len(companies) + 1)]
take = []

#dynamic programming recursive function
def pick(stock, comps, n):
#	print stock
#	print comps

	for i in range(1, n+1):
		for w in range(stock+1):
#			print i, w
			if(quantity[comps[i-1]] <= w and (price[comps[i-1]] + best[i-1][w-quantity[comps[i-1]]] > best[i-1][w])):
				best[i][w] = price[comps[i-1]] + best[i-1][w-quantity[comps[i-1]]]
				keep[i][w] = 1
			else:
				best[i][w] = best[i-1][w]
				keep[i][w] = 0

#	print best
#	print keep
	temp = supply
	for i in range(n, 0, -1):
		if(keep[i][temp] == 1):
			take.append(comps[i-1])
			temp = temp - quantity[comps[i-1]]
	return best[n][supply]

'''
#if there are no more companies to look at or if there is no more supply
	if n==0:
		return 0
	if stock == 0:
		return 0

#pop the last element in the list of companies
	last = comps[n-1]

#if there is not enough stock to fill the order, move on to the next one
	if stock - quantity[last] < 0:
		return pick(stock, comps, n-1)

#either choose the company or don't, build a tree of each of the possible combinations of companies
#whose orders will fit. Choose the path with the highest revenue in the end.
	else:
		sel = price[last] + pick(stock-quantity[last], comps, n-1)
		notsel = pick(stock, comps, n-1)
		if(sel > notsel):
			best[stock][n] = last
			return sel
		else:
			best[stock][n] = last
			return notsel

'''

n = len(companies)
rev = pick(supply, companies, n)
#print best
#print take
print 'Should complete the following orders:'
quant = 0
for s in take:
	print 'Company: ', s, '   Amount: ', quantity[s],'   Price: ', price[s]
	quant += quantity[s]
print 'Total Quantity: ', quant, 'Total Revenue: ', rev
