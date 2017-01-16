from utility import get_web_raw
from HTMLParser import HTMLParser
from utility import get_date_str
import os

class HtmlParserStockPrice(HTMLParser):
    
    FLAG_TABLE_START = False
    FLAG_NEW_STOCK = False
    DEFAULT_PREFIX_NAME = 'top'    
    TEMP_FILE = "./database/%s/%s_%s.stk"
    TF = None    
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
        self.parser_state = 0
        self.parser_substate = 0
    
    def set_file_prefix(self, prefix, stock_id):
        self.DEFAULT_PREFIX_NAME = ("%s_%s") % (prefix, stock_id) 
        
    def handle_starttag(self, tag, attrs):
        
        attrs_hash = dict(attrs)        
        try:                
            #First Table COntent
            if (tag == 'td') \
            and attrs_hash['align'] == 'center' \
            and attrs_hash['width'] == '105':
                if self.parser_substate == 0:                                        
                    self.parser_substate = 1                    
                    return
                
            if (tag == 'b') and (self.parser_substate == 1):
                self.parser_substate = 2 # Get stock price
                return   
            
            if (tag == 'font') and (self.parser_substate == 3):
                self.parser_substate = 4 # Get stock price
                return 
            
            if (tag == 'td') and (self.parser_substate == 6):                
                self.parser_substate = 7 # Get stock price
                return              
        except:
            pass
        
    def handle_endtag(self, tag):
        if tag == 'html':
            # Don't need to write file.
            #self.write_data_list(self.data_list)
            #self.data_list = []  # clear list
            pass

    
    def handle_data(self, data):
        # Get price 
        if self.parser_substate == 2:
            proc_data = data.strip()
            if proc_data != '':
                #print "INFO - [Get Field1]", proc_data
                self.data_list.append(proc_data)
                self.parser_substate = 3 # reset substate
                pass
       
        # Get +/- degree
        if self.parser_substate == 4: 
            proc_data = data.strip()
            if proc_data != '':
                #print "INFO - [Get Field2]", proc_data
                self.data_list.append(proc_data)
                self.parser_substate = 5 # reset substate
                #print "@74:", self.parser_substate
                pass        
        elif self.parser_substate == 5:
            self.parser_substate = 6
            #print "@80:", self.parser_substate
            #print "@81:", data.strip()
            proc_data = data.strip()
            if proc_data != '':
                #print "INFO - [Get Field3]", proc_data
                self.data_list.append(proc_data)
                self.parser_substate = 0 # reset substate
                #print "@83", self.parser_substate
                pass            
                            

    def write_data_list(self, data_list):  
        print "DEBUG - Write Date:", data_list     
        date_str = get_date_str(0)
        folder_name = date_str
        file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        print "DEBUG - File:", file_name
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

def analyze_price_html(prefix, stock_id):
    url = ('http://tw.stock.yahoo.com/q/q?s=%s') % stock_id      
    print url   
    html = get_web_raw(url)         
    parser = HtmlParserStockPrice()
    parser.set_file_prefix(prefix, stock_id)
    parser.feed(html)      
    print "INFO - analyze_price_html:", parser.data_list
    return parser.data_list
    
##############################################################
# main test
##############################################################                

if __name__ == '__main__':
    
    analyze_price_html('PRICE', '2498')
    print "DONE"
    pass                
                
                 
                
