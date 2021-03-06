import re
import math
import sqlite3
from sys import argv

script, filename, image_src, num_top_pages = argv
pages = dict() # keys = url : value = Page object

connect = sqlite3.connect('pages.sqlite')
c = connect.cursor()

class Page():
    ave_load = 0;
    standard_dev = 0;
    num_visits = 1;
    loadtimes = []

    def set_values(self, ave_load, standard_dev, visits):
        self.ave_load = ave_load
        self.standard_dev = standard_dev
        self.num_visits = visits

    def append(self,loadtime):
        self.loadtimes.append(loadtime)
 
    def get_aveload(self):
        return self.ave_load

    def get_standarddev(self):
        return self.standard_dev

    def get_visits(self):
        return self.num_visits

    def get_loadtimes(self):
        return self.loadtimes

    def print_values(self):
        print "ave = " + self.ave_load + " stand_dev = " + self.standard_dev + " visits = " + self.num_visits

    def print_loadtimes(self):
        print self.loadtimes

    def __str__(self):
        return str(self.ave_load) + ": " + str(self.standard_dev) + ": " + str(self.num_visits)


# open and read access.log file
def process_file(filename, img_src):
    request = ''
    file = open(filename, "r");
    
    for line in file:
        # get request
        split_log = line.split('\"');
        if len(split_log) > 1:
            request = (split_log[1].split(' '))[1];

        # get referer and update pages hashmap
        # only process this log if the http request contains the load time info
        if (request.startswith(img_src) and len(split_log) > 3):
            referer = split_log[3]

            if (referer != '-' ): 
                loadtime = get_loadtime(request, img_src)
                update_page(referer, loadtime)

    file.close()

# parse http request for load time
def get_loadtime(request, img_src):
    pattern = img_src + '\?loadtime='
    return re.sub(pattern, '', request)


# store or update page values     
def update_page(url, new_loadtime):
    new_loadtime = float(new_loadtime)
   
    # if page is already in list update values
    if (pages.has_key(url)):
        page = pages[url]
        ave_load = page.ave_load
        num_visits = page.num_visits

        print url
        print page
        page.append(new_loadtime)
        ave_load = ((num_visits * ave_load) + new_loadtime)/ (num_visits + 1)
        standard_dev = calc_standard_dev(page.get_loadtimes(), ave_load)

        page.set_values(ave_load, standard_dev, num_visits + 1)

        #print url + ": loadtime = " + new + "---",
        #print page

    # else add page to list
    else:
        new_page = Page()
        new_page.append(new_loadtime)
        new_page.set_values(new_loadtime, 0, 1) 
        
        pages[url] = new_page
        print url
        print pages[url]

        #print url + ": loadtime = " + new + "---",
        #print new_page,
        #print "------------NEW"

def calc_standard_dev(list, average):
    sum = 0

    if len(list) <= 1:
        return 0

    else:
        for x in list:
            sum = sum + math.pow((x-average), 2)
        print list
        print "sum = " + str(sum)    
        return math.sqrt(sum/(len(list)-1))
    
    

def sort_by_visits(amount):
    items = pages.items()
    sorted_by_visits = [ [page[1].get_visits(),page[0]] for page in items]
    sorted_by_visits.sort(reverse=True)

    print sorted_by_visits
    return get_most_visited(amount, sorted_by_visits)

# return the most visited pages
def get_most_visited(amount, list):

    if amount > len(list):
        amount = len(list)

    most_visited = []    
    for i in range(0,amount):
        url = list[i][1]
        most_visited.append([url,pages[url]])

    print most_visited
    return most_visited
   
# print each key:value pair in the pages hashmap
def print_pages():
    keys = pages.keys()

    for url in keys:
        print url
        print pages[url]

# Database Functions
def update_database():
    keys = pages.keys()

    # Insert data
    for url in keys:
        page = pages[url]
        c.execute("""INSERT INTO pages values (?,?,?,?,1)""", (str(url), page.get_aveload(), page.get_standarddev(), page.get_visits()))
        
    # Save the changes
    connect.commit()
    
def print_database():
    c.execute('SELECT * FROM pages ORDER BY num_visits')
    for row in c:
        print row
    
# Main
process_file(filename, image_src)
#sort_by_visits(num_top_pages)
print '\n'
print_pages()

print '\n'
#update_database()
#print_database()





