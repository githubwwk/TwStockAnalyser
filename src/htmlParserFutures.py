from utility import get_web_raw
from HTMLParser import HTMLParser
from utility import get_date_str
import utility
import os

##############################################################
# class HtmlParserFUT
############################################################## 
class HtmlParserFUT(HTMLParser):
    
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
        self.valid_data = 0
        self.indexTblCnt = 0
        self.file_name = ''
        
    def set_file_prefix(self, prefix):
        self.DEFAULT_PREFIX_NAME = prefix        
    
    def handle_starttag(self, tag, attrs):
        
        attrs_hash = dict(attrs)
        
        if self.parser_state == 0:        
            try:
                if (tag == 'tr') and (attrs_hash['class'] == '12bk'):
                    self.parser_state = 1                                    
                    pass
            except:
                pass  
                
        elif self.parser_state == 2:
            if (tag == 'font') and (attrs_hash['color'] == 'blue'):
                self.valid_data = 1                
            else:
                self.valid_data = 0                    
        
    def handle_endtag(self, tag):

        if (self.parser_state == 2) and (tag =='tr'):
            #self.FLAG_TABLE_START = False
            self.write_data_list(self.data_list)
            self.data_list = []  # clear list
            self.parser_state = 3 # end
            #print "state:", self.parser_state      
    
    def handle_data(self, data):
        #print data
        if (self.parser_state == 1) and (data == '外資'):
            self.parser_state = 2
        elif self.parser_state == 2:
            if self.valid_data == 1:
                data = data.strip()
                #data= data.replace(',','')
                self.data_list.append(data)
                #print data
            pass
        
    def write_data_list(self, data_list):  
        #print data_list     
        date_str = get_date_str(utility.DATE_STYLE_0)
        folder_name = date_str
        file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        self.file_name = file_name
        
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

##############################################################
# class HtmlParserFUTIndex
############################################################## 
class HtmlParserFUTIndex(HTMLParser):
            
    TF = None
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []        
        self.parser_state = 0 #0=get TWSE index, 1=get up/down stock NR        
        self.file_name = ''
        
    def set_filename(self, filename):
        self.file_name = filename        
    
    def handle_starttag(self, tag, attrs):    
        #attrs_hash = dict(attrs)
        pass
    
    def handle_endtag(self, tag):
        
        if (self.parser_state == 19) and (tag =='tr'):
            #self.FLAG_TABLE_START = False
            print "Write data to stk file!"
            self.write_data_list(self.data_list)
            self.data_list = []  # clear list
            self.parser_state += 1# end
            #print "state:", self.parser_state      
    
    def handle_data(self, data):        
        data = data.strip()        
        
        if (data == 'TX' and self.parser_state == 0):
            self.parser_state += 1            
        elif self.parser_state == 1:
            print "@1 ", data  
            self.parser_state += 1
        elif self.parser_state == 2:
            print "@2 ", data  
            self.data_list.append(data)
            self.parser_state += 1
        elif self.parser_state == 3:
            print "@3 ", data  
            self.parser_state += 1
        elif self.parser_state == 4:
            print "@4 ", data  
            self.parser_state += 1
        elif self.parser_state == 5:
            print "@5 ", data  
            self.parser_state += 1
        elif self.parser_state == 6:
            print "@6 ", data  
            self.parser_state += 1
        elif self.parser_state == 7:
            print "@7 ", data  
            self.parser_state += 1
        elif self.parser_state == 8:
            print "@8 ", data  
            self.parser_state += 1 
        elif self.parser_state == 9:
            print "@9 ", data  
            self.parser_state += 1 
        elif self.parser_state == 10:
            print "@10 ", data  
            self.data_list.append(data)
            self.parser_state += 1            
        elif self.parser_state == 11:
            print "@11 ", data  
            self.parser_state += 1  
        elif self.parser_state == 12:
            print "@12 ", data  
            self.parser_state += 1
        elif self.parser_state == 13:
            print "@13 ", data  
            self.data_list.append(data)
            self.parser_state += 1
        elif self.parser_state == 14:
            print "@14 ", data  
            self.parser_state += 1                                                                
            #self.data_list.append(data)   
        elif self.parser_state == 15:
            print "@15 ", data  
            self.parser_state += 1   
        elif self.parser_state == 16:
            print "@16 ", data  
            self.parser_state += 1                                    
        elif self.parser_state == 17:
            print "@17 ", data  
            self.data_list.append(data)
            self.parser_state += 1  
        elif self.parser_state == 18:
            print "@18 ", data  
            self.parser_state += 1                          
        
    def write_data_list(self, data_list):  
        #print data_list     
        #date_str = get_date_str(utility.DATE_STYLE_0)
        #folder_name = date_str
        #file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        
        file_name = self.file_name 
        
        if self.TF == None:
            file_dir = os.path.dirname(os.path.abspath(file_name))
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                print "DEBUG - [Raw date file dir]:", file_dir
        
        # Open result file
        self.TF = open(file_name, 'a')        
        #self.TF.write(get_date_str(utility.DATE_STYLE_4)+';')
        print "INFO - [Gen STK File]:", file_name
        for elmnt in data_list:
            elmnt = elmnt.rstrip(os.linesep)
            if elmnt != '':
                self.TF.write(elmnt+';')
        
        self.TF.close()
        
##############################################################
# API
############################################################## 

def analyze_futures_html(type_prefix): 
                
    url = gen_twse_url()
    #print "INFO - [FUT URL]:", url     
    html = get_web_raw(url)   
         
    #print html 
    parser = HtmlParserFUT()
    parser.set_file_prefix(type_prefix)
    parser.feed(html)      

    index_url = gen_twse_index_url()
    index_html = get_web_raw(index_url)
    parser2 = HtmlParserFUTIndex()
    parser2.set_filename(parser.file_name)
    parser2.feed(index_html)            

def gen_twse_url():    
    futures_url = 'http://www.taifex.com.tw/chinese/3/7_12_3.asp'
    print "INFO - [FUT URL]:", futures_url
    return futures_url

def gen_twse_index_url():
    futures_url = 'http://www.taifex.com.tw/chinese/3/3_1_1.asp'
    print "INFO - [FUT Index URL]:", futures_url
    return futures_url

##############################################################
# main test
##############################################################                

if __name__ == '__main__':
    
    analyze_futures_html('FUT')
    #str = '外資'
    #print str
    print "Done"
    pass                
                
                 
                
