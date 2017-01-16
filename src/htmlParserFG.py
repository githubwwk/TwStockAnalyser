from utility import get_web_raw
from HTMLParser import HTMLParser
from utility import get_date_str
import os

class HtmlParserFG(HTMLParser):
    
    FLAG_TABLE_START = False
    FLAG_NEW_STOCK = False
    DEFAULT_PREFIX_NAME = 'top'    
    TEMP_FILE = "./database/%s/%s_%s.stk"
    TF = None
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
    
    def set_file_prefix(self, prefix):
        self.DEFAULT_PREFIX_NAME = prefix
        
    def handle_starttag(self, tag, attrs):
        
        attrs_hash = dict(attrs)
        if self.FLAG_TABLE_START:
            print("@@@@@@");
            try:
                if attrs_hash['bgcolor'] == '#FFFFFF':
                    self.FLAG_NEW_STOCK = True
                    # Next stock date
            except:
                pass
        else:
            try:                
                #First Table COntent
                if (tag == 'table') \
                and attrs_hash['border'] == '0' \
                and attrs_hash['width'] == '600' \
                and attrs_hash['cellpadding'] == '3' \
                and attrs_hash['cellspacing'] == '1':                    
                    self.FLAG_TABLE_START = True
            except:
                pass
        
    def handle_endtag(self, tag):
        if self.FLAG_TABLE_START:
            if tag == 'table':
                self.FLAG_TABLE_START = False
                self.write_data_list(self.data_list)
                self.data_list = []  # clear list
            if (self.FLAG_NEW_STOCK == True) and (tag == 'tr'):
                self.FLAG_NEW_STOCK = False
    
    def handle_data(self, data):
        if self.FLAG_TABLE_START and self.FLAG_NEW_STOCK:
            proc_data = data.strip()
            if proc_data != '':
                #print "INFO - [Get Field]", proc_data
                self.data_list.append(proc_data)
                pass

    def write_data_list(self, data_list):  
        #print data_list     
        date_str = get_date_str(0)
        folder_name = date_str
        file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        
        if self.TF == None:
            file_dir = os.path.dirname(os.path.abspath(file_name))
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                print "DEBUG - [Raw date file dir]:", file_dir
        
        # Open result file
        self.TF = open(file_name, 'w')
        print "INFO - [Gen STK File]:", file_name
        for elmnt in data_list:
            elmnt = elmnt.rstrip(os.linesep)
            if elmnt != '':
                self.TF.write(elmnt+';')
        
        self.TF.close()

def analyze_fg_html(prefix, url):         
    html = get_web_raw(url)   
    print "DEBUG: html:%s" % html;   
    parser = HtmlParserFG()
    parser.set_file_prefix(prefix)
    parser.feed(html)      
        
##############################################################
# main test
##############################################################                
import codecs

if __name__ == '__main__':
    print("Start");
    analyze_fg_html('TSE_FGB', 'tw.stock.yahoo.com/d/i/fgbuy_tse50.html')
    
    pass                
                
                 
                
