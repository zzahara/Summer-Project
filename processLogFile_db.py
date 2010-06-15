import re
import math
import sqlite3 
from sys import argv

script, filename, image_src, num_top_pages = argv

connect = sqlite3.connect('pages.sqlite')
c = connect.cursor()
next_id = 0

table_cols = {'user':'STRING', 'page':'STRING', 'loadtime':'INTEGER', 'locale':'STRING', 'referer':'STRING', 'timestamp':'INTEGER', 'useragent':'STRING'}

def init():
    # delete table and indicies
    keys = table_cols.keys()
    c.execute(""" DROP TABLE IF EXISTS pages;""")
    for col in keys:
       c.execute("DROP INDEX IF EXISTS " + col + "_index;")

    # create string for fields and types
    count = 0
    columns = []
    
    for col in keys:
        col_type = col + ' ' + table_cols[col]
        columns.append(col_type)
    values = ', '.join(columns)
        

    # create table and an index for each column
    c.execute("CREATE TABLE IF NOT EXISTS pages(" + values + ");")
    for col in keys:
       c.execute("CREATE INDEX IF NOT EXISTS " + col+ "_index ON pages(" + col + ");")

    connect.commit()

def get_input():
    filename = rawinput("Enter log file: ")
    image_src = rawinput("Enter image source: ")
    num_top_pages = rawinput("Enter the number of top pages: ")

def process_file(filename, img_src):
    request = ''
    file = open(filename, "r")

    # referer must be 2 or more chars to avoid "-" referers
    pattern = '(?P<user>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [^ ]+ [^ ]+ \[(?P<timestamp>../.../....:..:..:.. .....)\] ' + '"GET (?P<bug>' + img_src + '[^"]+)" (?P<status>\d{3}) (?P<size>[^ ]+) "(?P<page>[^"]{2,})" "(?P<useragent>[^"]+)"'
    c = re.compile(pattern)

    for log_line in file:
        m = c.match(log_line)
        if m:
            page_data = m.groupdict()
            bug_values = get_values(page_data['bug'], img_src)

            page_data.update(bug_values)
            
            #print page_data
            update_database(page_data)
    file.close()
            
def get_values(bug, img_src):
    end = bug.replace(img_src + '?', '')
    bug_values = dict(item.split("=") for item in end.split("&"))
    return bug_values

def update_database(page_values):
    keys = table_cols.keys()
    values = []

    for col in keys:
        print col + ':'
        print page_values[col]
        values.append(page_values[col])
        
    c.execute("""INSERT INTO pages values (?,?,?,?,?,?,?)""", (values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
    connect.commit()

# read log file, parse out loadtimes and urls, and store in database
def process_file2(filename, img_src):
    request = ''
    file = open(filename, "r");

    for line in file:
        # get request
        split_log = line.split('\"');
        if len(split_log) > 1:
            request = (split_log[1].split(' '))[1];

        # get referer and store in database
        # only process this log if the http request contains the load time info
        if (request.startswith(img_src) and len(split_log) > 3):
            referer = split_log[3]

            if (referer != '-'): 
                loadtime = get_loadtime(request, img_src)
                update_database(referer, loadtime);

    file.close()

# parse http request for load time
def get_loadtime(request, img_src):
    pattern = img_src + '\?loadtime='
    return re.sub(pattern, '', request)

# store a new page into the database
def update_database2(referer, loadtime):
    global next_id
    c.execute("""SELECT id FROM pages where url = ?""", (referer,))
    id = c.fetchone()

    if id == None:
        #print 'none: next_id =  ' + str(next_id) + 'url= ' + referer
        c.execute("""INSERT INTO pages values (?,?,?)""", (next_id, referer, loadtime))
        next_id = next_id + 1
    else:
        #print str(id) + ' ' + str(referer)
        c.execute("""INSERT INTO pages values (?,?,?)""", (id[0], referer, loadtime))

    connect.commit()
       
def process_database():
    global next_id
    i = 0
    
    for i in range(0, next_id):
        print str(i) + ' ',
        c.execute("""SELECT url from pages where id = ?""", (i,))
        url = c.fetchone()[0]

        c.execute("""SELECT loadtime from pages where id = ?""", (i,)) 
        loadtimes = c.fetchall()

        ave_load = calc_aveload(loadtimes)
        standard_dev = calc_standard_dev(loadtimes, ave_load)
    
        print url + ': ',
        print ' ' + str(ave_load) + ': ' + str(standard_dev)

        

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
    
    
def print_database():
    c.execute('SELECT * FROM pages ORDER BY id')
    for row in c:
        print row
    
init()        
process_file(filename, image_src)
#process_database()

c.close()

