import utility
import os
import shutil
from utility import get_date_str

class reportStockAll:
    DEFAULT_PREFIX_NAME = 'stockall'    
    TEMP_FILE = "./report/%s/%s_%s.txt"
    
    def __init__(self, stock_list):    
        self.write_file(stock_list)
        pass
    
    def __write_tbl_title(self, hFile):
        hFile.write('ID;')
        hFile.write('NAME;')
        hFile.write('Price;')
        hFile.write('Value;')
        hFile.write('P-V;')     # Calculate by code              
        hFile.write('EPS-Q1;')
        hFile.write('EPS-Q2;')
        hFile.write('EPS-Q3;')
        hFile.write('EPS-Q4;')
        hFile.write('ROI(%);')   # Calculate by code
        hFile.write('PER;')      # Calculate by code  
        hFile.write('EPS-Y1;')
        hFile.write('EPS-Y2;')
        hFile.write('EPS-Y3;')
        hFile.write('EPS-Y4;')   
        for i in range(10):
            hFile.write('CDIV-Y' + str(i) + ';')    
        for i in range(10):
            hFile.write('SDIV-Y' + str(i) + ';')   
        hFile.write('\r\n')  
    
    def write_file(self,stock_list):
             
        date_str = get_date_str(0)
        folder_name = date_str
        file_name = (self.TEMP_FILE) % (folder_name, self.DEFAULT_PREFIX_NAME, date_str)
        
        file_dir = os.path.dirname(os.path.abspath(file_name))        
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            print "DEBUG - [Raw date file dir]:", file_dir
        
        # Open result file
        hFile = open(file_name, 'w')
        print "INFO - [Gen STK File]:", file_name
        
        self.__write_tbl_title(hFile)
        
        i = 0    
        for sk in stock_list:                        
            hFile.write(sk.id + ';')
            hFile.write(sk.name + ';')
            hFile.write(sk.price + ';')
            hFile.write(sk.value + ';')
            
            try:
                ## Price - Value
                pv= float(sk.price) - float(sk.value)
                hFile.write(str(pv) + ';')            
            except:
                hFile.write('NG' + ';')
                  
            eps_4q_sum = 0
            for i in range(4):
                try:
                    hFile.write(sk.recent_quarter_eps[i] + ';')              
                    eps_4q_sum = eps_4q_sum + float(sk.recent_quarter_eps[i])     
                except:
                    hFile.write('NG' + ';')      
                    eps_4q_sum = eps_4q_sum + 0              
            try:                    
                ## Return On Investment ROI
                div_sum = float(sk.stock_dividend[0]) + float(sk.cash_dividend[0])    
                ROI = (div_sum / float(sk.price)) * 100
                ROI_STR = "%.2f" % ROI
                hFile.write(str(ROI_STR) + ';') 
            except:
                hFile.write('NG' + ';')
            
            try:     
                ## PER PE Ratio
                PER = float(sk.price)/eps_4q_sum
                PER_STR = "%.2f" % PER
                hFile.write(PER_STR + ';') 
            except:
                hFile.write('NG' + ';')
                
            for i in range(4):
                try:                    
                    hFile.write(sk.recent_year_eps[i] + ';')
                except:
                    hFile.write('NG' + ';')
                    
            for i in range(10):    
                try:                    
                    hFile.write(sk.cash_dividend[i] + ';')
                except:
                    hFile.write('NA' + ';')

            for i in range(10):    
                try:                    
                    hFile.write(sk.stock_dividend[i] + ';')
                except:
                    hFile.write('NA' + ';')
             
            hFile.write('\r\n')       
            
            #i = i+1
            #if i > 10:
            #    break              
            #break
                        
        hFile.close()    
            
        pass

    
    
##############################################################
# main test
##############################################################

if __name__ == '__main__':        
    pass
