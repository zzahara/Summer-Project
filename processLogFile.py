import re
from sys import argv

script, filename, image_src = argv
pages = dict() # keys = url : value = Page object

class Page():
    ave_load = 0;
    standard_dev = 0;
    num_visits = 1;

    def set_values(ave, sd, visits):
        ave_load = ave
        standard_dev = sd
        num_visits = visits

    # doesn't work when printing elements in hashmap?  
    def __str__():
        return str(self.ave_load)


# open and read access.log file
def process_file(filename, img_src):
    
    file = open(filename, "r");
    line = file.readline();

    for line in file:

        # get request
        split_log = line.split('\"');
        request = (split_log[1].split(' '))[1];

        # get referer and update pages hashmap
        # only process this log if the http request is for the load time image
        if (request.startswith(img_src) and len(split_log) > 3):
            referer = split_log[3]
            if (referer != '-' ): update_page(referer, 1)

    file.close()


# store or update page values     
def update_page(url, new_loadtime):
   
    # if page is already in list update values
    if (pages.has_key(url)):
        value = pages[url]
        ave_load = value.ave_load
        num_visits = value.num_visits

        value.ave_load = ((num_visits * ave_load) + new_loadtime)/ (num_visits + 1)
        value.num_visits = num_visits + 1
        value.standard_dev = 0

    # else add page to list
    else:
        new_page = Page()

        # results in TypeError: set_values() takes exactly 3 arguments (4 given) ????
        # new_page.set_values(new_loadtime, 0, 1) 

        new_page.ave_load = new_loadtime
        new_page.standard_dev = 0
        pages[url] = new_page


def print_pages():
    print pages.items()
    

process_file(filename, image_src)
print_pages()



