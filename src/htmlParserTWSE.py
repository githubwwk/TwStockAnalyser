from utility import get_web_raw
from HTMLParser import HTMLParser
from utility import get_date_str
import utility
import os

class HtmlParserTWSE(HTMLParser):
    
    FLAG_TABLE_START = False
    FLAG_NEW_STOCK = False
    DEFAULT_PREFIX_NAME = 'top'    
    TEMP_FILE = "./database/%s/%s_%s.stk"    
    TF = None
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
        self.dataCnt = 0
        self.parser_state = 0 #0=get TWSE index, 1=get up/down stock NR
        self.parser_substate = 0
        self.indexTblCnt = 0
        
    def set_file_prefix(self, prefix):
        self.DEFAULT_PREFIX_NAME = prefix
        
    def handle_starttag_twse_index(self, tag, attrs):
        attrs_hash = dict(attrs)
        
    
    def handle_starttag_twse_updown_nr(self, tag, attrs):            
                    
        pass
    
    def handle_starttag(self, tag, attrs):
                    
        if self.parser_state == 0:
            self.handle_starttag_twse_index(tag, attrs)
        elif self.parser_state == 1:
            self.handle_starttag_twse_updown_nr(tag, attrs)
            
        return        
        
    def handle_endtag(self, tag):

        if tag == 'html':
            #self.FLAG_TABLE_START = False
            self.write_data_list(self.data_list)
            self.data_list = []  # clear list
                
        if (self.FLAG_NEW_STOCK == True) and (tag == 'tr'):
            self.FLAG_NEW_STOCK = False
    
    
    def handle_data_twse_updown_nr(self, data):
        if self.FLAG_TABLE_START and self.FLAG_NEW_STOCK:
            proc_data = data.strip()
            if proc_data != '' and ('(' in proc_data):
                #print "self.dataCnt:", self.dataCnt
                #print "INFO - [Get Field]", proc_data
                self.data_list.append(proc_data)
                self.FLAG_TABLE_START = False                
                self.dataCnt = 0 
                pass
        
        if self.parser_state == 2:
            print "INFO - [Index]:", data.strip()
    
    def handle_data_twse_index(self, data):
        proc_data = data.strip()
        if (proc_data != '') and (self.parser_substate == 2) and (self.indexTblCnt == 2):
            self.dataCnt += 1            
            self.data_list.append(proc_data)
            print "DEBUG - proc_date:", proc_data
            if self.dataCnt >= 3:      # Get index, mode +/- (Rose/Fall), degree
                self.parser_state = 1  # Next state, Get TWSE UP/DOWN NR
                self.dataCnt = 0
        pass
    
    def handle_data(self, data):
        proc_data = data.strip()
        
        if proc_data == '發行量加權股價指數':
        	self.parser_state = 1            
        elif self.parser_state == 1:                        
            self.parser_state += 1                 
        elif self.parser_state == 2:
            print "@@@1", proc_data            
            self.parser_state += 1  
            self.data_list.append(proc_data)                     
        elif self.parser_state == 3:
            print "@@@2", proc_data                    
            self.parser_state += 1            
        elif self.parser_state == 4:
            print "@@@3", proc_data
            self.data_list.append(proc_data)
            self.parser_state += 1   
        elif self.parser_state == 5:
            print "@@@4", proc_data            
            self.parser_state += 1 
        elif self.parser_state == 6:
            print "@@@5", proc_data
            self.data_list.append(proc_data)
            self.parser_state += 1
        
        if proc_data == '上漲(漲停)':
            self.parser_state = 10
        elif self.parser_state == 10:
            self.parser_state += 1
        elif self.parser_state == 11:
            self.parser_state += 1
        elif self.parser_state == 12:
            self.parser_state += 1
        elif self.parser_state == 13:
            self.parser_state += 1
            self.data_list.append(proc_data)
            print "@up  ", proc_data

        if proc_data == '下跌(跌停)':
            self.parser_state = 20 
        elif self.parser_state == 20:
            self.parser_state += 1
        elif self.parser_state == 21:
            self.parser_state += 1
        elif self.parser_state == 22:
            self.parser_state += 1
            #print "@115 ",  proc_data    
        elif self.parser_state == 23:
            self.parser_state += 1
            print "@down ",  proc_data
            self.data_list.append(proc_data)                              	               
        
    def write_data_list(self, data_list):  
        #print data_list     
        date_str = get_date_str(utility.DATE_STYLE_0)
        folder_name = date_str
        file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        
        if self.TF == None:
            file_dir = os.path.dirname(os.path.abspath(file_name))
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                print "DEBUG - [Raw date file dir]:", file_dir
        
        # Open result file
        self.TF = open(file_name, 'w')
        self.TF.write(get_date_str(utility.DATE_STYLE_4)+';')
        print "INFO - [Gen STK File]:", file_name
        for elmnt in data_list:
            elmnt = elmnt.rstrip(os.linesep)
            if elmnt != '':
                self.TF.write(elmnt+';')
        
        self.TF.close()

def analyze_twse_html(type_prefix): 
                
    url = gen_twse_url()
    #print "INFO - [TWSE URL]:", url 
     
    html = get_web_raw(url)     
    #print html 
    parser = HtmlParserTWSE()
    parser.set_file_prefix(type_prefix)
    parser.feed(html)      

def gen_twse_url():
    #twse_today_url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/genpage/Report201408/A11220140822MS.php?select2=MS&chk_date=103/08/22' 
    #twse_today_url = ('http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/genpage/Report%s/A112%sMS.php?select2=MS&chk_date=%s') % (get_date_str(1), get_date_str(0), get_date_str(2)) 
    twse_today_url = ('http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php')
    print "INFO - [TWSE URL]:", twse_today_url
    return twse_today_url

##############################################################
# main test
##############################################################                

if __name__ == '__main__':
    
    analyze_twse_html('TWSE')
    
    pass                
                
                 
                
