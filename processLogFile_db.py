import re
import math
import sqlite3 
from sys import argv

script, filename, image_src, num_top_pages = argv
num_top_pages = int(num_top_pages)

connect = sqlite3.connect('pages.sqlite')
c = connect.cursor()

#table_cols2 = {'user':'STRING', 'page':'STRING', 'loadtime':'INTEGER', 'locale':'STRING', 'referer':'STRING', 'timestamp':'INTEGER', 'useragent':'STRING'}
cols_n_type = [('user', 'STRING'), ('page', 'STRING'), ('loadtime', 'INTEGER'), ('locale', 'STRING'), ('referer', 'STRING'), ('timestamp', 'INTEGER'), ('useragent', 'STRING')]
table_cols = 'user, page, loadtime, locale, referer, timestamp, useragent'

def init():
    # delete table and indicies
    c.execute(""" DROP TABLE IF EXISTS pages;""")

    for i in range(0, len(cols_n_type)):
        c.execute("DROP INDEX IF EXISTS " + cols_n_type[i][0] + "_index;")
    
    connect.commit()

    # create string for fields and types
    columns = []
    for i in range(0, len(cols_n_type)):
        col_type = cols_n_type[i][0] + ' ' + cols_n_type[i][1]
        columns.append(col_type)

    values = ', '.join(columns)

    # create table and an index for each column
    c.execute("CREATE TABLE IF NOT EXISTS pages(" + values + ");")
    for i in range(0, len(cols_n_type)):
        col = cols_n_type[i][0]
        c.execute("CREATE INDEX IF NOT EXISTS " + col + "_index ON pages(" + col + ");")

    connect.commit()    

def get_input():
    filename = rawinput("Enter log file: ")
    image_src = rawinput("Enter image source: ")
    num_top_pages = rawinput("Enter the number of top pages: ")

def process_file(filename, img_src):
    request = ''
    file = open(filename, "r")

    # \S = shortcut for non whitespace
    pattern = '(?P<user>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [^ ]+ [^ ]+ \[(?P<timestamp>../.../....:..:..:.. .....)\] ' + '"GET (?P<bug>' + img_src + '[^"]+)" (?P<status>\d{3}) (?P<size>[^ ]+) "(?P<page>[^"]+)" "(?P<useragent>[^"]+)"'
    c = re.compile(pattern)

    for log_line in file:
        m = c.match(log_line)
        
        if m:
            page_data = m.groupdict()

            if page_data['page'] == "-":
                continue
            bug_values = get_values(page_data['bug'], img_src)
            page_data.update(bug_values)
            
            #print page_data
            update_database(page_data)
        #else:
            #print 'REJECTING ' + log_line
    file.close()
            
def get_values(bug, img_src):
    end = bug.replace(img_src + '?', '')
    bug_values = dict(item.split("=") for item in end.split("&"))
    return bug_values

# ------------------------------------------------------------
#                     Database Functions
# ------------------------------------------------------------

def update_database(page_values):
    global table_cols
    values = []

    for i in range(0, len(cols_n_type)):
        col = cols_n_type[i][0]
        value = page_values[col]
        values.append(value)
    
    c.execute("INSERT INTO pages (" + table_cols + ") values (?,?,?,?,?,?,?)", (values))
    connect.commit()

def num_users():
    c.execute("""SELECT COUNT(DISTINCT user) from pages""")
    return c.fetchone()[0]
    
    # check the speed diff between these two
    #c.execute(""" SELECT DISTINCT user from pages """)
    #return len(c.fetchall())

def total_page_views():
    c.execute("""SELECT COUNT(*) from pages""")
    return c.fetchone()[0]

    #c.execute(""" SELECT * from pages """)
    #return len(c.fetchall())
    
def page_views(page):
    c.execute("SELECT COUNT(*) from pages where page = '" + page + "'")
    return c.fetchone()[0]

    #c.execute(" SELECT * from pages where page = '" + page + "'")
    #return len(c.fetchall())

def process_database2():
    global num_top_pages
    c.execute(""" SELECT DISTINCT page from pages """)
    pages = c.fetchall()

    # top_pages[x][0] = # of views
    # top_pages[x][1] = page
    top_pages = get_top_pages(pages)
    print top_pages
    print ''
    print len(top_pages)

    if len(top_pages) < num_top_pages:
        num_top_pages = len(top_pages)

    for i in range(0, num_top_pages):
        c.execute("SELECT loadtime from pages where page = '" + top_pages[i][1] + "'")
        loadtimes = c.fetchall()

        ave_load = calc_aveload(loadtimes)
        standard_dev = calc_standard_dev(loadtimes, ave_load)

        print top_pages[i][1] + ': ',
        print ' ' + str(ave_load) + ': ' + str(standard_dev)

def get_top_pages(pages):
    top_pages = []

    for url in pages:
        c.execute("SELECT * from pages where page = '" + url[0] + "'")
        data = c.fetchall()
        top_pages.append((len(data), url[0]))
        
    top_pages.sort()
    top_pages.reverse()
    return top_pages
            
       
def process_database():
    i = 0
    
    for i in range(0, 6):
        print str(i) + ' ',
        c.execute("""SELECT url from pages where id = ?""", (i,))
        url = c.fetchone()[0]

        c.execute("""SELECT loadtime from pages where id = ?""", (i,)) 
        loadtimes = c.fetchall()

        ave_load = calc_aveload(loadtimes)
        standard_dev = calc_standard_dev(loadtimes, ave_load)
    
        print url + ': ',
        print ' ' + str(ave_load) + ': ' + str(standard_dev)

# ------------------------------------------------------------
#                     Reporting Functions
# ------------------------------------------------------------        

def calc_aveload(loadtimes):
    i = 0
    sum = 0.0
    
    for i in range(i, len(loadtimes)):
        sum = sum + loadtimes[i][0]

    return sum/len(loadtimes)

def calc_standard_dev(values, average):
    sum = 0

    if len(values) <= 1:
        return 0

    else:
        for value in values:
            x = value[0]
            sum = sum + math.pow((x-average), 2)

        return math.sqrt(sum/(len(values)-1))

#def calc_bounce_rate():
    
        
def print_database():
    c.execute('SELECT * FROM pages ORDER BY id')
    for row in c:
        print row
    
init()        
process_file(filename, image_src)

#print "len(c.fetchall()) WAY"
#print "COUNT() WAY"
print 'num users = ' + str(num_users())
print 'total views = ' + str(total_page_views())
print 'yahoo.com: ' + str(page_views("http://www.yahoo.com"))
print 'bbc.com: ' + str(page_views("http://www.bbc.com"))
print 'time.com: ' + str(page_views("http://www.time.com"))
#process_database2()

c.close()

