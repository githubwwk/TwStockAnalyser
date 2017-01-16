from utility import get_web_raw
from HTMLParser import HTMLParser
from utility import get_date_str
import os

class HtmlParserStockList(HTMLParser):
    
    FLAG_TABLE_START = False
    FLAG_NEW_STOCK = False
    DEFAULT_PREFIX_NAME = 'top'    
    TEMP_FILE = "./database/%s/%s_%s.stk"
    TF = None    
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
        self.parser_getdata = False        
        self.parser_substate = 0
    
    def set_file_prefix(self, prefix, stock_id):
        self.DEFAULT_PREFIX_NAME = ("%s_%s") % (prefix, stock_id) 
        
    def handle_starttag(self, tag, attrs):
        
        if (self.parser_substate < 0):
            return
        
        attrs_hash = dict(attrs)        
        try:                
            #First Table COntent
            if (tag == 'td') \
            and attrs_hash['height'] == '20' \
            and attrs_hash['class'] == 'basic2' \
            and attrs_hash['align'] == 'center' :                            
                self.parser_substate = 1                                                 
                self.parser_getdata = True                                                                   
                return                                                                                                          
        except:
            pass
        
    def handle_endtag(self, tag):
        if (tag == 'html') and (self.parser_substate > 0):
            # Don't write to file.
            #self.write_data_list(self.data_list)
            #self.data_list = []  # clear list            
            #print "DEBUG - Write File (State):", self.parser_substate
            self.parser_substate = -1
        
    
    def handle_data(self, data):
        # Get price 
        if self.parser_getdata == True:
            proc_data = data.strip()
            if proc_data != '':
                #print "INFO - [Get Data]", proc_data
                self.data_list.append(proc_data)                
                pass        
            
            self.parser_getdata = False
                            

    def write_data_list(self, data_list):  
        print "DEBUG - Write Date:", data_list     
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
        
def analyze_stocklist_html(prefix):
    url = ('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php')         
    html = get_web_raw(url)   
    #print html      
    parser = HtmlParserStockList()
    parser.set_file_prefix(prefix, 'all')
    parser.feed(html)  
    return parser.data_list    
        
##############################################################
# main test
##############################################################                

if __name__ == '__main__':
    
    analyze_stocklist_html('STOCKLIST')
    
    pass                
                
                 
                
