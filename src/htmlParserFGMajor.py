from utility import get_web_raw
from HTMLParser import HTMLParser
import utility
import os

class HtmlParserFGMajor(HTMLParser):
    
    TD_FGTSE_VAL_STATE = 0
    TD_FGOTC_VAL_STATE = 0
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
        if self.TD_FGTSE_VAL_STATE == 1:            
            try:
                if (tag == 'font') \
                and attrs_hash['color'] == '#FF0000':
                    self.TD_FGTSE_VAL_STATE = 2                    
                    # Next stock date                    
            except:                
                pass
        elif self.TD_FGOTC_VAL_STATE == 1:            
            try:
                if (tag == 'font') \
                and attrs_hash['color'] == '#FF0000':
                    self.TD_FGOTC_VAL_STATE = 2                    
                    # Next stock date                    
            except:                
                pass            
        else:
            try:                
                #First Table COntent
                if (tag == 'td') \
                and attrs_hash['width'] == '570' \
                and attrs_hash['align'] == 'CENTER' \
                and attrs_hash['colspan'] == '7' \
                and attrs_hash['class'] == 'ttt':                    
                    self.TD_FGTSE_VAL_STATE = 1                    
                    
                if (tag == 'td') \
                and attrs_hash['width'] == '480' \
                and attrs_hash['align'] == 'center' \
                and attrs_hash['colspan'] == '3' \
                and attrs_hash['class'] == 'ttt':                    
                    self.TD_FGOTC_VAL_STATE = 1                                    
            except:
                pass
        
    def handle_endtag(self, tag):
        if self.TD_FGTSE_VAL_STATE == 3 and self.TD_FGOTC_VAL_STATE == 3:            
            if tag == 'table':                                
                self.write_data_list(self.data_list)
                self.TD_FGTSE_VAL_STATE = 0
                self.TD_FGOTC_VAL_STATE = 0                
    
    def handle_data(self, data):
        if self.TD_FGTSE_VAL_STATE == 2:
            proc_data = data.strip()
            #print "@@", proc_data
            if proc_data != '':
                print "INFO - [Get Field]", proc_data
                self.data_list.append(proc_data)
                self.TD_FGTSE_VAL_STATE = 3
                pass

        if self.TD_FGOTC_VAL_STATE == 2:
            proc_data = data.strip()
            #print "@@", proc_data
            if proc_data != '':
                print "INFO - [Get Field]", proc_data
                self.data_list.append(proc_data)
                self.TD_FGOTC_VAL_STATE = 3
                pass
            

    def write_data_list(self, data_list):  
        #print data_list     
        date_str = utility.get_date_str(0)
        folder_name = date_str
        file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        
        if self.TF == None:
            file_dir = os.path.dirname(os.path.abspath(file_name))
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                print "DEBUG - [Raw date file dir]:", file_dir
        
        # Open result file
        print "INFO - [Gen STK File]:", file_name
        self.TF = open(file_name, 'w')        
        self.TF.write(utility.get_date_str(utility.DATE_STYLE_4)+';')
        #self.TF.write('13/09/05;')
        for elmnt in data_list:
            elmnt = elmnt.rstrip(os.linesep)
            if elmnt != '':
                self.TF.write(elmnt+';')
        
        self.TF.close()

def analyze_fgmajor_html(prefix, url):         
    html = get_web_raw(url)      
    parser = HtmlParserFGMajor()
    parser.set_file_prefix(prefix)
    parser.feed(html)      
        
##############################################################
# main test
##############################################################                

if __name__ == '__main__':
    
    analyze_fgmajor_html('FG_MAJOR', 'http://tw.stock.yahoo.com/d/i/major.html')
    
    pass                
                
                 
                
