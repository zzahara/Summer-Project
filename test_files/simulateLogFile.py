# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

# usage: python simulateLogFile.py [log file]


import re
import random
from sys import argv 

script, filename = argv

fields = ['user', ' - ', '- ', 'timestamp', ' "GET ', 'request', '" ', 'status', ' ', 'size', ' "', 'page', '" "', 'useragent', '"']

referrers = ['http://www.cs.usfca.edu', 'http://www.yahoo.com', 'http://www.google.com', 
    'http://archive.org', 'http://blahblah.com', 'http://www.netflix.com', 
    'http://www.harrypotter.com', 'http://www.movies.com', 'http://helloworld.com',
    'http://www.about.com']

locales = ['sq_AL', 'sq', 'ar_DZ', 'ar_BH', 	'ar_EG', 'ar_IQ', 'es-US', 'ar_KW', 'ar_LB', 'ar_LY', 
    'ar_MA', 'ar_OM', 'es-US', 'ar_SA', 'ar_SD', 'ar_SY', 'ar_TN', 'es-US', 'ar', 'be_BY', 'be',
    'bg_BG', 'bg', 'ca_ES', 'ca', 'zh_CN', 'zh_HK', 'zh_SG', 'zh_TW', 'zh', 	'hr_HR', 'hr', '	cs_CZ', 
    'en-US', 'es-US', 'tr', 'vi']


def random_bug():
    values = dict()
    args = ['loadtime', 'referrer', 'locale']
    bug = 'http://analytics.archive.org/0.gif?'

    ref_index = random.randint(0, len(referrers)-1)
    loc_index = random.randint(0, len(locales)-1)

    values['loadtime'] = random.randint(1,100)
    values['referrer'] = referrers[ref_index]
    values['locale'] = locales[loc_index]

    for i in range(0, len(args)):
        if i != 0:
            bug = bug + '&'
        arg = args[i]
        bug = bug + arg + '=' + str(values[arg])

    return bug
    
def generate_log():
    file = open(filename, "r")

    bug = [True, False]
    
    for log_line in file:
        if bug[random.randint(0,1)]:

            pattern = '(?P<user>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [^ ]+ [^ ]+ (?P<timestamp>\[../.../....:..:..:.. .....\]) "GET (?P<bug>[^"]+)" (?P<status>\d{3}) (?P<size>[^ ]+) "(?P<page>[^"]+)" "(?P<useragent>[^"]+)"'
            c = re.compile(pattern)
            m = c.match(log_line)

            if m:
                log = ''
                log_dict = m.groupdict()

                for field in fields:
                    log_dict['request'] = random_bug()
                    
                    if log_dict.has_key(field):
                        log = log + log_dict[field]
                    else:
                        log = log + field

                print log
        else:
            print log_line, 
                
    file.close()

# Main
generate_log()

    






