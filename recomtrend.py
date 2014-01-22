#!/usr/bin/python

import csv, urllib, sys

nxt = 0

def get_page():

    # Open the Yahoo Finance! analyst opinion section of the selected stock code
    try:
        stockurl = "http://finance.yahoo.com/q/ao?s="+str(sys.argv[1])+"+Analyst+Opinion"
        return  urllib.urlopen(stockurl).read()
    except:
        print "Error !! Invalid Stock Code..."
        return ""
    return ""


def get_next_analyst_value(page):
	    
    global nxt
    nxt += 1
    start_link = page.find('Recommendation Trends')
    if nxt == 1:
        start_link = page.find('Recommendation Trends')
        if start_link == -1: 
            return None, 0
    elif nxt > 1 and nxt <= 20: 
        start_link = page.find('center"')     
       
    start_quote = page.find('center">', start_link)
    end_quote = page.find('</td', start_quote + 1)
    analyst_value = page[start_quote + 8:end_quote]
    return analyst_value, end_quote


def get_all_analyst_values(page):
	    
    # Fetch the recommendation trend values of the particular stock 
    analyst_values_list = []
    while True:
        analyst_value,endpos = get_next_analyst_value(page)
        if analyst_value:
            analyst_values_list.append(analyst_value)
            page = page[endpos:]
        else:
            break
    return analyst_values_list
    

def recommendation_trend_calculator():

	"""
	Computed the weighted average using emperical assigned weights as follows:
	Strongly Buy -5, Buy 4, Hold - 3, Underperform - 2, Sell -1
	Also,
		curmon - current month
		lamon  - last month
		twomon - two months ago
		thrmon - three months ago
	"""
	x,curmon_total,lamon_total,twomon_total,thrmon_total = 0,0,0,0,0
	while (x < 20):
	    curmon_total += float(a[0 + x])
	    lamon_total  += float(a[1 + x])
	    twomon_total += float(a[2 + x])
	    thrmon_total += float(a[3 + x])
	    if x < 16 :
	        x += 4
	    else:
	        break

	x,y,curmon,lamon,twomon,thrmon = 0,5.0,0,0,0,0
	while (x < 20 and y > 0):
	    curmon += y * float(a[0 + x])
	    lamon  += y * float(a[1 + x])
	    twomon += y * float(a[2 + x])
	    thrmon += y * float(a[3 + x])
	    if x < 16:
	        x += 4
	    else:
	        break
	    y -= 1.0

	cm = []
	cm.append(0.0) if curmon_total == 0.0 else cm.append((curmon/curmon_total)*1.0)
	cm.append(0.0) if lamon_total  == 0.0 else cm.append((lamon /lamon_total )*0.3678)
	cm.append(0.0) if twomon_total == 0.0 else cm.append((twomon/twomon_total)*0.1353)
	cm.append(0.0) if thrmon_total == 0.0 else cm.append((thrmon/thrmon_total)*0.0497)
	return cm


def write_news_indicator(filename, cm):
		
	#write the computed values in a CSV file
	f = open(filename, 'wt')
	try:
		writer = csv.writer(f)
		writer.writerow(['Current_Month', 'Last_Month', 'Two_Months_Ago', 'Three_Months_Ago'])
		curmon_term = str(cm[0]).encode('ascii', 'ignore')
		lamon_term  = str(cm[1]).encode('ascii', 'ignore')
		twomon_term = str(cm[2]).encode('ascii', 'ignore')
		thrmon_term = str(cm[3]).encode('ascii', 'ignore')
		writer.writerow([curmon_term, lamon_term, twomon_term, thrmon_term])
	finally:
		f.close()
		print "Finished writing " + sys.argv[1] + " News Indicator CSV file."


if __name__ == "__main__":
	
	a = get_all_analyst_values(get_page())
	cm = recommendation_trend_calculator()
	filename = 'News_Indicator_' + sys.argv[1] +'.csv'
	write_news_indicator(filename, cm)
