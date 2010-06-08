import re
from sys import argv

script, filename, image_src = argv
pages = dict()

class Page():
    ave_load = 0;
    standard_dev = 0;
    num_visits = 1;

    
    def __str__():
        return str(self.ave_load)



# open and read access.log file
def process_file(filename, img_src):
    
    file = open(filename, "r");

    line = file.readline();
    for line in file:

        #print line
        # get request
        split_list = line.split('\"');
        request = (split_list[1].split(' '))[1];
        

        if (request.startswith(img_src)):
            #print split_list

            # get referer, if there is one
            if (len(split_list) > 3):
                #print request
                referer = split_list[3]
                #print referer + '\n'
                if (referer != '-' ): update_page(referer, 1)

    file.close()

# store referer and other info     
def update_page(referer, new_loadtime):
   
    # if in list update values
    if (pages.has_key(referer)):
        data = pages[referer]
        ave_load = data.ave_load
        num_visits = data.num_visits

        data.ave_load = ((num_visits * ave_load) + new_loadtime)/ (num_visits + 1)
        data.num_visits = num_visits + 1
        data.standard_dev = 0

    # else add page to list
    else:
        new_page = Page()
        new_page.ave_load = new_loadtime
        new_page.standard_dev = 0
        pages[referer] = new_page


def print_pages():
    print pages.items()
    

process_file(filename, image_src)
print_pages()


print "End of Program"


