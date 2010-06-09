import random
from sys import argv 

script, size = argv

pages = ['http://www.cs.usfca.edu', 'http://www.yahoo.com', 'http://www.google.com', 
    'http://archive.org', 'http://blahblah.com', 'http://www.netflix.com', 
    'http://www.harrypotter.com', 'http://www.movies.com', 'http://helloworld.com',
    'http://www.about.com', '-']

requests = ['http://analytics.archive.org/archive.gif', 'http://archive.org',
    'http://analytics.archive.org/archive.gif', 'http://cnn.com', 'http://download.com',
    'http://analytics.archive.org/archive.gif', 'http://wikipedia.org', 'http://ww.craigslist.com',
    'http://analytics.archive.org/archive.gif', 'http://www.weather.com', 'http://facebook.com',
    'http://bbc.com', 'http://www.weather.com', 'http://analytics.archive.org/archive.gif']

def random_request():
    index = random.randint(0, len(requests)-1)
    return requests[index]

def random_page():
    index = random.randint(0, len(pages)-1)
    return pages[index]

    
def generate_log():
    i = 0
    for i in range(0, int(size)):

        request = random_request()
        if request == 'http://analytics.archive.org/archive.gif':
            loadtime = random.randint(1,100)
            request = request + '?loadtime=' + str(loadtime)

        print "0.6.103.74 - userid [04/Jun/2010:00:02:51 +0000] \"GET",
        print request + "\" 302 57893 \"" + random_page() + "\"",
        print "\"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.19) Gecko/2010031422 Firefox/3.0.19 (.NET CLR 3.5.30729)\""
  

# Main
generate_log()

    
    






