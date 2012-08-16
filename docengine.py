import datetime
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
    #print m.group(1)
    print type(docResults[contents])
    try:
        c3 = m.group(3)
    except:
        c3 = None
    if c3 != None:
        pass #print c3

    if type(docResults[contents]) == type(datetime.datetime.now()):
        result = docResults[contents]
        c3 = dateFormat(c3)
        return result.strftime(c3)
    else:
        return '{}'.format(docResults[contents]) 

def fillGets(xml, dictionary):
    xml = re.sub('\[get\((.*?)\)\]', formatGet ,xml)
    xml = re.sub('\[MERGEFIELD (.*?)(\s"(.*)")?\]', formatGet ,xml)
    #   \[[\s*]?MERGEFIELD[\s*]?(.*?)([\s*]?"(.*)?")?[\s*]?\]
    return xml
    
def dateFormat(format):
    dateFormatTable = [
                       ('YYYY' , '%Y' ),
                       ('YY' , '%y' ),
                       ('WW' , '%A' ),
                       ('W' , '%a' ),
                       ('MMMM' , '%B' ),
                       ('MMM' , '%b' ),
                       ('MM' , '%m' ),
                       ('M' , '%m' ),
                       ('HH:MM' , '%x' ),
                       ('HH' , '%I' ),
                       ('DD' , '%d' ),
                       ('D', '%d' ) 
                      ]
    
    if format == None:
        return '%x'
    else:
        for i in dateFormatTable:
            format = str.replace(format, i[0], i[1])
        return format

# import datetime
# now = datetime.datetime.now()
# dateformat = dateFormat('MM-DD-YY WW, MMMM DD, YYYY')
# print now.strftime('%s' % dateformat)


xml = getDoc(askvalue['docid']) 
docResults  = getDocQuery(xml)
xml = removeQuery(xml)
xml = fillGets(xml, docResults)

print xml



#print (results)
#Documentquery RegEx  '(?<=\[DOCUMENTQUERY).*(?=\])'
#Get Regex '(?<=\[get\().*?(?=\)\])'

#Get Regex from J '\[get\((.*?)\)\]'
#                   replace $1


    
    


#x = getDocQuery(xml)
#print x





































