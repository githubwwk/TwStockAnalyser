
from htmlParserStockList import analyze_stocklist_html
from htmlParserStockPrice import analyze_price_html
from htmlParserStockDetailInfo import analyze_detail_html
from htmlParserStockDividend import analyze_dividend_html
from reportStockAll import reportStockAll
from config import config 
import utility
import time
##############################################################
# Class
##############################################################
class stock:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.price = ''
        self.value = ''
        self.alist = []
        self.recent_quarter_eps = []
        self.recent_year_eps = []
        self.cash_dividend = []
        self.stock_dividend = []
               
class TwAllStockAnalyzer:
    
    def __get_tw_all_stock_id(self, stock_list):
        temp_list = analyze_stocklist_html('STOCKLIST')
 
        #################
        ## Konrad Test ##
 #       sk = stock()
 #       sk.id = '8042'
 #       sk.name = 'EVA AIR'
 #       stock_list.append(sk)
 #       return 
        #################
        for idx, value in enumerate(temp_list):
            if (idx % 2) == 0:
                sk = stock()   
                sk.id = value    # Set Stock ID                          
                #print sk.id
            else:
                sk.name = value  # Set Stock Name                           
                #print sk.name  
                stock_list.append(sk)                      
        pass
    
    def __set_stock_price(self, sk):        
        temp_list =  analyze_price_html('PRICE', sk.id) 
        try:
            sk.price = temp_list[0]
        except:
            sk.price = 'NG'        
        
    def __remove_eps_chinese(self, str):
        ret_str = str[0:-3]
        return ret_str
        
    def __remove_value_chinese(self,str):
        ret_str = str[14:-3]
        return ret_str
        
    def __set_detailinfo(self, sk):
        temp_list = analyze_detail_html('DETAIL', sk.id)
        
        if (temp_list == None):
            return -1
        
        try:
        #if (True):        
            sk.recent_quarter_eps.append(self.__remove_eps_chinese(temp_list[1]))                                        
            sk.recent_quarter_eps.append(self.__remove_eps_chinese(temp_list[5]))
            sk.recent_quarter_eps.append(self.__remove_eps_chinese(temp_list[9]))
            sk.recent_quarter_eps.append(self.__remove_eps_chinese(temp_list[13]))
             
            sk.recent_year_eps.append(self.__remove_eps_chinese(temp_list[3]))
            sk.recent_year_eps.append(self.__remove_eps_chinese(temp_list[7]))
            sk.recent_year_eps.append(self.__remove_eps_chinese(temp_list[11]))
            sk.recent_year_eps.append(self.__remove_eps_chinese(temp_list[15]))
            
            sk.value = self.__remove_value_chinese(temp_list[-1])
            
#             print "DEBUG - Stock [id]:%s " % (sk.id)
#             print "DEBUG - Stock [price]:%s " % (sk.price)
#             print "DEBUG - Stock [value]:%s" % sk.value
#             print "DEBUG - Stock [recent_quarter_eps]:%s" % sk.recent_quarter_eps
#             print "DEBUG - Stock [recent_year_eps]:%s" % sk.recent_year_eps
        except:
            print "ERROR - Invalid Stock Detail [id]:%s [info]:%s" % (sk.id, temp_list)
        
        return 0
                                 
    
    def __set_dividend(self, sk):
        temp_list = analyze_dividend_html('DIVIDEND', sk.id)
        try:
            for i in range(0, len(temp_list), 3):                
                sk.cash_dividend.append(temp_list[i+1])
                sk.stock_dividend.append(temp_list[i+2])
            #end for
#             print "DEBUG - Stock [cash_dividend]:%s" % sk.cash_dividend
#             print "DEBUG - Stock [stock_dividend]:%s" % sk.stock_dividend
            
        except:
            print "ERROR - Invalid Stock Detail [id]:%s [info]:%s" % (sk.id, temp_list)
            pass
        pass
    
    def __init__(self):
        self.stock_list = []
        
        # init stock_list
        self.__get_tw_all_stock_id(self.stock_list)
        i = 0
        for sk in self.stock_list:                       
            self.__set_stock_price(sk)
            
            if self.__set_detailinfo(sk) != 0:
                print "ERROR - Terminate Fetch!" 
                break
            
            self.__set_dividend(sk)            
            #print "DEBUG - Stock [id]:%s [name]:%s [price]:%s" % (sk.id, sk.name, sk.price)
            print "%s" % (sk.id)           
            # For test
            #i = i+1
            #if i > 10:
            #    break    
            time.sleep(1)
        report = reportStockAll(self.stock_list)        
        pass
        
##############################################################
# main test
##############################################################

if __name__ == '__main__':    
    
    stockAnlyzer = TwAllStockAnalyzer()
    
    print "INFO - Done"
    pass  
