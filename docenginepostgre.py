import datetime
import re
import pymssql      # MSSQL
# import psycopg2   # Postgre

askvalue = {'docid': 10,
            'ORDER_NUMBER': '10250'}
listNumCount = []
activeDictonary = {}


def sqlData(sql, dict=False):
    '''returns data from any sql query'''
    conn = pymssql.connect(host='server\sql2008', user='python',
                           password='sql', database='northwind',
                           as_dict='True')
    # conn = psycopg2.connect('dbname=postgres user=postgres')  #Postgre
    cur = conn.cursor()
    cur.execute('%s' % sql)
    return cur.fetchall()


def getDoc(docid):
    '''returns xml data from a given docid'''
    xml = sqlData('select xml from dbo.xml where pkid = %s' % docid)
    a = xml.pop()
    return a['xml']   # MSSQL
    # return a        # Postgre


def removeQuery(xml):
    '''clears any queries from the document after retrieving the data'''
    xml = re.sub('\[DOCUMENTQUERY.*?\]', '', xml)
    return xml


def getDocQuery(docString):
    '''finds any DOCUMENTQUERY Strings and returns a dictionary with SQL
       column names and values'''
    docQuery = re.findall('(?<=\[DOCUMENTQUERY ").*?(?="\])',
                          '%s' % docString)

    a_dict = {}
    for item in docQuery:
        sqlQuery = re.sub('~ASKVALUE (.*?)~',
                          lambda m: '{}'.format(askvalue[m.group(1)]),
                          item)
        result = sqlData('%s' % sqlQuery)
        a_dict.update(result.pop())
    return a_dict


def formatGet(m):
    '''Determines what format to use for values based on variable type
    '''
    global activeDictonary
    contents = m.group(1)
    #print m.group(1)
    #print type(docResults[contents])
    try:
        c3 = m.group(2)
    except:
        c3 = None
    if c3 != None:
        pass  # print c3
    try:
        if type(activeDictonary[contents]) == type(datetime.datetime.now()):
            result = activeDictonary[contents]
            c3 = dateFormat(c3)
            return result.strftime(c3)
        else:
            return '{}'.format(activeDictonary[contents])
    except:
        return '***ERROR RETRIEVING %s***' % contents


def fillGets(xml, dictionary):
    '''Finds all [get(VALUE)] and [MERGEFIELD VALUES] in xml and
       replaces them with the values found in the passed dictionary.
    '''
    global activeDictonary
    activeDictonary = dictionary
    xml = re.sub('\[get\((.*?)\)\]', formatGet, xml)
    xml = re.sub('\[MERGEFIELD (.*?)(?:\s"(.*)")?\]', formatGet, xml)
    #   \[[\s*]?MERGEFIELD[\s*]?(.*?)([\s*]?"(.*)?")?[\s*]?\]
    return xml


def dateFormat(format):
    ''' Used by formatGet, this converts Docmaster date formatting to
        python date formatting.

        DMS date formatting is commented below

        Todo: AM/PM Modifiers, Minutes
    '''
    dateFormatTable = [
                       ('YYYY', '%Y'),   # 2012 - 4 Digit Year
                       ('YY', '%y'),     # 12   - 2 Digit Year
                       ('WW', '%A'),     # Tuesday - Day of Week
                       ('W', '%a'),      # Tue  - Short Day of Week
                       ('MMMM', '%B'),   # August - Month
                       ('MMM', '%b'),    # Aug  - Short Month
                       ('MM', '%m'),     # 08   - Month Number
                       ('M', '%m'),      # 08   - Month Number (Legacy)
                       ('HH:MM', '%x'),  # 11:47 - Time
                       ('HH', '%I'),     # 11   - Hour
                       ('DD', '%d'),     # 04   - Day of Week
                       ('D', '%d')       # 04   - Day of Week (Legacy)
                      ]

    if format == None:
        return '%m/%d/%Y'
    else:
        for i in dateFormatTable:
            format = str.replace(format, i[0], i[1])
        return format


def formatListNum(m):
    ''' Used by fillListNum to count each List and return an int value

        To do: Roman Numeral Format Type, may need new function,
               or new markup language.
    '''
    global listNumCount
    listNumCount.append(m.group(1))
    c = listNumCount.count(m.group(1))
    return '%s' % c
    pass


def fillListNum(xml):
    ''' Finds all LISTNUM markup and replaces it with sequential numbers
    '''
    return re.sub('\[LISTNUM (.*?)(\s"(.*)")?\]', formatListNum, xml)


def fillMergeLoops(xml):
    global docResults
    text = ''
    regexMatch = re.finditer('\[MERGELOOP "(.*?)"(?:\s"(.*?)")?](.*?)\[ENDMERGE\]',
                           xml,
                           re.DOTALL)

    for item in regexMatch:
        text = ''
        print item.group(1, 2, 3)
#        loopQuery = fillGets(item.group(1), docResults)
#        loopData = sqlData(loopQuery)
#        loopText = item.group(2)
#        activeDictonary = loopData
#        for item in loopData:
#            text = text + fillGets(loopText, loopData)

#        xml = xml.replace(item.group(1), text)
#        print text
#    return xml


xml = getDoc(askvalue['docid'])
docResults = getDocQuery(xml)
xml = removeQuery(xml)
fillMergeLoops(xml)
xml = fillGets(xml, docResults)
xml = fillListNum(xml)


print xml







