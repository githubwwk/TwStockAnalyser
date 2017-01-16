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
        self.parser_getdata = False  
        self.parser_checktitle = False 
        self.invalid_content = False 
        self.parser_substate = 0
    
    def set_file_prefix(self, prefix, stock_id):
        self.DEFAULT_PREFIX_NAME = ("%s_%s") % (prefix, stock_id) 
        
    def handle_starttag(self, tag, attrs):
        
        if (self.parser_substate < 0):
            return
        
        attrs_hash = dict(attrs)        
        try:                
            #First Table COntent
            if (tag == 'table') \
            and attrs_hash['width'] == '630' \
            and attrs_hash['border'] == '0' \
            and attrs_hash['cellspacing'] == '1' \
            and attrs_hash['cellpadding'] == '4' :
                if self.parser_substate == 0:                                                      
                    self.parser_substate = 1    
                    #print "DEBUG - Sub-state:", self.parser_substate                                                                    
                    return                  
                                                                                 
            if (self.parser_substate == 5):
                if tag == 'td' and attrs_hash['align'] == 'center':
                    self.parser_substate = 1                     
                    self.parser_getdata = True
                    return 
                                                
            if (self.parser_substate == 4):
                if tag == 'td' and attrs_hash['bgcolor'] == '#FFFAE8':
                    self.parser_substate = 5                     
                    self.parser_getdata = True
                    return 
                                                
            if (self.parser_substate == 3):
                if tag == 'td' and attrs_hash['align'] == 'center':
                    self.parser_substate = 4                     
                    self.parser_getdata = True
                    return   
                                                
            if (tag == 'td') and attrs_hash['bgcolor'] == '#FFFAE8' and (self.parser_substate == 1):
                self.parser_substate = 2                
                return            
            
            if (self.parser_substate == 2):
                if (tag == 'td') and attrs_hash['bgcolor'] == '#FFFAE8':                   
                    self.parser_substate = 3 
                    self.parser_getdata = True        
                    return

            if (tag == 'td') \
            and attrs_hash['colspan'] == '4' \
            and attrs_hash['bgcolor'] == '#FFFfff' \
            and attrs_hash['align'] == 'left':
                self.parser_getdata = True
                return   
            
            if (tag == 'title'):                
                self.parser_checktitle = True                                                    
        except:
            pass
        
    def handle_endtag(self, tag):
        if tag == 'table' and (self.parser_substate > 0):
            # Don't need to write file.
            #self.write_data_list(self.data_list)
            #self.data_list = []  # clear list            
            #print "@@@", self.parser_substate
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
        
        if self.parser_checktitle == True:
            if '999 Unable to process' in data:
                print "ERROR - Yahoo Protection: %s" % data 
                self.invalid_content = True
            self.parser_checktitle = False                

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

def analyze_detail_html(prefix, stock_id):
    url = ('http://tw.stock.yahoo.com/d/s/company_%s.html') % stock_id
    print url           
    html = get_web_raw(url)   
    #print html      
    
    parser = HtmlParserStockPrice()
    parser.set_file_prefix(prefix, stock_id)
    parser.feed(html)      
    
    if parser.invalid_content == True:
        return None
    else:
        print "DEBUG - data_list", parser.data_list
        return parser.data_list
        
##############################################################
# main test
##############################################################                

if __name__ == '__main__':
    
    analyze_detail_html('DETAIL', '2498')
    print "TEST Done"
    pass                
                
                 
                
