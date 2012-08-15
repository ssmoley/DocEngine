import re
import pymssql

askvalue = {'docid':7,
			'ORDER_NUMBER':'10250' }


def sqlData(sql, dict = False):
	'''returns data from any sql query'''
	conn = pymssql.connect(host='server\sql2008', user='python', password='sql', database='northwind', as_dict='True')
	cur = conn.cursor()	

	cur.execute('%s' % sql)

	return cur.fetchall()

def getDoc(docid):
	'''returns xml data from a given docid'''
	xml = sqlData('select xml from xml where pkid = %s' % docid)
	a = xml.pop()
	return a['xml']
	
def removeQuery(xml):
	xml = re.sub('\[DOCUMENTQUERY.*?\]','',xml)
	return xml
	
def getDocQuery(docString):
	docQuery = re.findall('(?<=\[DOCUMENTQUERY ").*?(?="\])','%s' % docString)

	a_dict = {}
	for item in docQuery:
		sqlQuery = re.sub('~ASKVALUE (.*?)~', lambda m: '{}'.format(askvalue[m.group(1)]) ,item)
		result = sqlData('%s' % sqlQuery)
		a_dict.update(result.pop())
	return a_dict

def formatGet(m):
	contents = m.group(1)
	print m.group(1)
	try:
		c2 = m.group(2)
	except:
		c2 = None
	try:
		c3 = m.group(3)
	except:
		c3 = None
	print contents
	if c2 != None:
		print c2 
	if c3 != None:
		print c3
	return '{}'.format(docResults[contents]) 

def fillGets(xml, dictionary):
	xml = re.sub('\[get\((.*?)\)\]', formatGet ,xml)
	xml = re.sub('\[MERGEFIELD (.*?)(\s"(.*)")?\]', formatGet ,xml)
	print xml

	
	
xml = getDoc(askvalue['docid'])	
docResults	= getDocQuery(xml)
xml = removeQuery(xml)
fillGets(xml, docResults)
#print (results)
#Documentquery RegEx  '(?<=\[DOCUMENTQUERY).*(?=\])'
#Get Regex '(?<=\[get\().*?(?=\)\])'

#Get Regex from J '\[get\((.*?)\)\]'
#					replace $1


	
	


#x = getDocQuery(xml)
#print x





































