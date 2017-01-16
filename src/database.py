import os
from config import config 
from utility import read_file
from utility import list_all_file
##############################################################
# Global Variable
##############################################################
NO_EXIST_CHAR = '= '
##############################################################
# FGDailyDB class
##############################################################
class FGDailyDB:
    
    ROW_DATA_NR =0  # how many date in a row.
    
    def __init__(self, type, filename):
        self.stock_name_list = []
        self.stock_id_list = []
        
        self.type = type
        self.filename = filename
        
        if('TSE' in type):
            self.ROW_DATA_NR = 7
        elif('OTC' in type):
            self.ROW_DATA_NR = 6
        
        self.__proc(filename)
    

    def __proc(self, filename):
        
        file_data = read_file(filename)
        data_list = file_data.split(';')
        cnt = 0
        for value in data_list:
            if (cnt % self.ROW_DATA_NR) == 1 :
                stock_name = value[4:]
                stock_id = value[0:4]
                self.stock_name_list.append(stock_name)
                self.stock_id_list.append(stock_id)
            cnt += 1
        
        pass

    def is_exist_id(self, stock_id):
        if stock_id in self.stock_id_list:
            return True
        else:
            return False
##############################################################
# StockHistory class
##############################################################
class StockHistory:    
    
    def __init__(self, type):
        # Keep current process buy or sell type.
        if ('FGS' in type):
            self.type = 'S'
        elif('FGB' in type):
            self.type = 'B'
        
        self.fg_daily_db_list = []
    
    def add_fg_daily(self, fg_daily):
        self.fg_daily_db_list.append(fg_daily)

    def get_latest_fg_daily(self):
        print "INFO - [Last Daily DB]:", self.fg_daily_db_list[0].filename
        return self.fg_daily_db_list[0]
        
    def get_history_result(self, stock_id):
        result = []
        # traverse all FG daily db.
        for daily in self.fg_daily_db_list:
            if daily.is_exist_id(stock_id) == True:
                result.append(self.type)  # Add BUY or SELL tag.
            else:                
                result.append(NO_EXIST_CHAR)
        
        return result
                
##############################################################
# database class
##############################################################
class database:
    DB_RAW_SUBFILE_NAME = '.stk'    
    VALID_DAYS = 40 # default setting
    
    OUTPUT_TXT_TYPE  = 0
    OUTPUT_HTML_TYPE = 1
    
    def __init__(self, db_dir, valid_days, type_list):
        self.stock_history_hash = {}
        self.VALID_DAYS = valid_days
        self.type_list = type_list
        self.__proc(db_dir)
        pass
    
    def __proc(self, db_dir):
        for type in self.type_list:
            stock_history = StockHistory(type)
            #db_file_list = self.__list_all_raw_file(db_dir, type)
            db_file_list = list_all_file(db_dir, type, self.DB_RAW_SUBFILE_NAME)
            for db_file in db_file_list[0:self.VALID_DAYS]:                
                fg_daily = FGDailyDB(type, db_file)
                stock_history.add_fg_daily(fg_daily)
            
            self.stock_history_hash[type] = stock_history            
    
    def get_stock_history(self, stock_id, out_type):
        
        conclusion_list = None
        result_one_list = []
        ret_string = ''
        
        for key, value in self.stock_history_hash.iteritems():
            fg_history_obj = value
            result_one_list = fg_history_obj.get_history_result(stock_id)            
            if conclusion_list == None:
                conclusion_list = result_one_list
            
            for index, value in enumerate(result_one_list):
                if (conclusion_list[index] == None) or ((conclusion_list[index] == NO_EXIST_CHAR)):
                    conclusion_list[index] = result_one_list[index]
        
        #print "INFO - [conslusion list]:", conclusion_list
        if (out_type == self.OUTPUT_HTML_TYPE):
            for state in conclusion_list:
                if state == 'B':
                    state = '<font color=\"red\" face=\"Consolas\">B</font>'
                elif state == 'S':
                    state = '<font color=\"green\" face=\"Consolas\">S</font>'
                else:
                	state = '<font color=\"black\" face=\"Consolas\">=</font>'
                
                ret_string += state + ''
        else:
            ret_string = conclusion_list 
        return ret_string
    
    # Return last date, stock id and stock name list.
    def get_last_stock_info(self, type):
        stock_id = []
        stock_name = []
        try:
            stock_history = self.stock_history_hash[type]
            fg_daily = stock_history.get_latest_fg_daily()
            stock_id = fg_daily.stock_id_list
            stock_name = fg_daily.stock_name_list
        except:
            stock_id = None
            stock_name = None
            
        return (stock_id, stock_name)
    
##############################################################
# main test
##############################################################

if __name__ == '__main__': 
    
    type_list = ['OTC_FGB', 'OTC_FGS', 'TSE_FGB', 'TSE_FGS']
    cfg = config('./config/setting.xml')
    db = database(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), type_list)   
    
    print db.get_stock_history('2888', database.OUTPUT_TXT_TYPE)
    print db.get_last_stock_info('OTC_FGB')
    print db.get_last_stock_info('OTC_FGS')
    print db.get_last_stock_info('TSE_FGB')
    id_list, name_list =  db.get_last_stock_info('TSE_FGS')
    
     
   
