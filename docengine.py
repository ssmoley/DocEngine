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
	

def fillGets(xml, dictionary):
	xml = re.sub('\[get\((.*?)\)\]', lambda m: '{}'.format(dictionary[m.group(1)]) ,xml)
	xml = re.sub('\[MERGEFIELD (.*?)\]', lambda m: '{}'.format(dictionary[m.group(1)]) ,xml)
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





































