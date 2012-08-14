
def sqlData(sql, dict = False):

	import pymssql
	conn = pymssql.connect(host='server\sql2008', user='python', password='sql', database='northwind', as_dict='True')
	cur = conn.cursor()	

	cur.execute('%s' % sql)

	return cur.fetchall()

def getDoc(docid):
	xml = sqlData('select xml from xml where pkid = %s' % docid)
	return xml.pop()


def getDocQuery(docString):
	import re
	docQuery = re.findall('(?<=\[DOCUMENTQUERY ").*?(?="\])','%s' % docString)
	return docQuery
	#print docQuery.group(0)
	
	
a = getDoc(2)	
	
#x = getDocQuery(a)

#Documentquery RegEx  '(?<=\[DOCUMENTQUERY).*(?=\])'
#Get Regex '(?<=\[get\().*?(?=\)\])'

#Get Regex from J '\[get\((.*?)\)\]'
#					replace $1

xml = a['xml']


x = getDocQuery(xml)
print x

#print type(xml)
#for a.rowcount in a:
#	pass #print 'XML = %s' % (row['XML'](0:500))
	

