import re
from sys import argv

script, filename, image_src = argv
pages = dict() # keys = url : value = Page object

class Page():
    ave_load = 0;
    standard_dev = 0;
    num_visits = 1;

    def set_values(self, ave_load, standard_dev, visits):
        self.ave_load = ave_load
        self.standard_dev = standard_dev
        self.num_visits = visits

    def print_values(self):
        print "ave = " + self.ave_load + " sd = " + self.standard_dev + " visits = " + self.num_visits

    # doesn't work when printing elements in hashmap?  
    def __str__(self):
        return str(self.num_visits)

    def __int__(self):
        return self.num_visits


# open and read access.log file
def process_file(filename, img_src):
    
    file = open(filename, "r");
    line = file.readline();

    for line in file:

        # get request
        split_log = line.split('\"');
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
    new = new_loadtime
    new_loadtime = float(new_loadtime)
   
    # if page is already in list update values
    if (pages.has_key(url)):
        value = pages[url]
        ave_load = value.ave_load
        num_visits = value.num_visits

        value.ave_load = ((num_visits * ave_load) + new_loadtime)/ (num_visits + 1)
        value.num_visits = num_visits + 1
        value.standard_dev = 0

        print url + ": " + new + ", " + str(value.ave_load)
        #print "visits = " + str(num_visits) + " ave_load = " + str(ave_load)

        # DEBUGGING
        #prev = (num_visits * ave_load)
        #num = (num_visits * ave_load) + new_loadtime
        #denom = (num_visits + 1)
        #print " computing values: prev = " + str(prev) + " num = " + str(num) + " denom = " + str(denom)

    # else add page to list
    else:
        new_page = Page()
        new_page.set_values(new_loadtime, 0, 1) 
        pages[url] = new_page

        print url + ": " + str(new_page.ave_load) + ", " + new + "------------NEW"

def sort_loadtimes():
    items = pages.items()

    sorted_by_visits = [ [int(page[1]),page[0]] for page in items]
    sorted_by_visits.sort(reverse=True)
    print sorted_by_visits

    return sorted_by_visits

# return the most visited pages
def get_most_visited(amount, list_by_visits):
    # will finish
     
    
   
# print each key : value pair in the pages hashmap
def print_pages():
    keys = pages.keys()

    for url in keys:
        print url
        print pages[url]
    
# main
process_file(filename, image_src)
#print_pages()
sort_loadtimes()


