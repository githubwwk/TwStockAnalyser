import datetime
import urllib 
import urllib2 
import os

DATE_STYLE_0 = 0
DATE_STYLE_1 = 1
DATE_STYLE_2 = 2
DATE_STYLE_3 = 3
DATE_STYLE_4 = 4

##############################################################
# get_date_str: Get date string 
############################################################## 

def get_date_str(style):
    now = datetime.datetime.now()
    date_str = ''
    if style == DATE_STYLE_0:
        date_str =("%04d%02d%02d") % (now.year, now.month, now.day)
    elif style == DATE_STYLE_1:
        date_str =("%04d%02d") % (now.year, now.month)
    elif style == DATE_STYLE_2:
        taiwan_year = now.year - 1911
        date_str =("%03d/%02d/%02d") % (taiwan_year, now.month,  now.day) 
    elif style == DATE_STYLE_3:
        date_str =("%02d%02d%02d") % ((now.year-2000), now.month, now.day)
    elif style == DATE_STYLE_4:
        date_str =("%02d/%02d/%02d") % ((now.year-2000), now.month, now.day)
        
    return date_str

##############################################################
# get_web_raw: Get web html content
############################################################## 
import httplib

def get_web_raw(url):
    
    if (url.find('https://') > -1):
        return get_https_web_raw(url)
            
    content = ''
    
    try:
        content = urllib.urlopen(url).read()     
      
    except IOError, e:
     
        print ("ERROR - HTTP Error!")
        return ""
    
    #content = content.decode('big5').encode('UTF-8')
    #content = content.decode('gb2312').encode('UTF-8')
    
    return content

def get_https_web_raw(url):
    
    content = ''
    host = url[len('https://'):url.index('/', len('https://'))] 
    page = url[url.index('/', len('https://')) : ]
    print host, page
    try:        
        
        c = httplib.HTTPSConnection(host)
        c.request("GET", page)    
        response = c.getresponse()
        print response.status, response. reason
        content = response.read()                
                
    except IOError, e:
        if hasattr(e, 'code'):
            print 'http error code:', e.code
        elif hasattr(e, 'reason'):
            print 'cant connect, reason:' , e.reason
        else:
            raise   
    
        print ("ERROR - HTTP Error!")
        return ""
    
    #content = content.decode('big5').encode('UTF-8')
    #content = content.decode('gb2312').encode('UTF-8')
    
    return content
##############################################################
# read_file: read file content to string
############################################################## 

def read_file(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return data

##############################################################
# is_weekend: checking today whether is a weekend
##############################################################

def is_weekend():
    day = datetime.datetime.today().weekday()
    if(day == 6) or (day == 5):
        #Sunday and Saturday
        return True
    else:
        return False

def current_hour():    
    now = datetime.datetime.now()    
    return now.hour

##############################################################
# is_weekend: checking today whether is a weekend
##############################################################
def list_all_file(dir, prefix, postfix):
        
    file_list = []
         
    for r, d, f in os.walk(dir):
            
        for files in f:                
            if r.find('expired') > 0:
                continue
            if files.endswith(postfix) \
            and files.startswith(prefix):
                file_dir = os.path.join(r, files)
                file_list.append(file_dir)
                #print "INFO - [Add DB File]:", file_dir
            else:
                pass
        
    file_list.sort()
    file_list.reverse()
    return file_list

##############################################################
# main test
##############################################################  

if __name__ == '__main__':
    
    #print get_date_str(0)
    #print get_date_str(1)
    #print get_date_str(2)
    print get_web_raw('https://tw.stock.yahoo.com/d/i/fgbuy_tse50.html')
    
    pass  