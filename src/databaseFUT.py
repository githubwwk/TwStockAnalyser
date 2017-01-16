import os
from config import config 
from utility import read_file
from utility import list_all_file


    
##############################################################
# TWSEInfo
##############################################################
class FUTInfo:
    
    #VALID_DATA_NR = 11
    
    def __init__(self, dbfile):
        self.Date = ''
        self.long_posi_con = ''
        self.short_posi_con = ''
        self.delta_posi_con = ''
        self.open_long_posi_con = ''
        self.open_short_posi_con = ''
        self.delta_open_posi_con = ''
        
        self.TWFUT_name = ''
        self.TWFUT_index =''
        self.TWFUT_index_updown = ''
        self.TWFUT_index_ud_percentage = ''
        
        self.__load(dbfile)
        pass

    def __load(self, dbfile):
        file_data = read_file(dbfile)        
        data_list = file_data.split(';')
       
        #if (len(data_list) != self.VALID_DATA_NR):
        #    print "ERROR - Invalid TWSE DB content." 
        self.Date   = data_list[0] 
        self.long_posi_con  = data_list[1]
        self.short_posi_con = data_list[2] 
        self.delta_posi_con  = data_list[3]    
        self.open_long_posi_con = data_list[4]   
        self.open_short_posi_con = data_list[5]     
        self.delta_open_posi_con = data_list[6]   
        
        data_list_len = len(data_list) - 1 ## sub last ';'
        
        print "DEBUG - [dbfile]:%s [data_list_len]:%d" % (dbfile, data_list_len)
        if (data_list_len >= 8) and (data_list_len <= 11):         
            self.TWFUT_name = data_list[7]
            self.TWFUT_index = data_list[8]
            self.TWFUT_index_updown = data_list[9]
            self.TWFUT_index_ud_percentage = data_list[10]                                   
        pass

    def show(self):
        print "self.Date:", self.Date
        print "self.long_posi_con:", self.long_posi_con
        print "self.short_posi_con:", self.short_posi_con
        print "self.delta_posi_con:", self.delta_posi_con 
        print "self.open_long_posi_con:", self.open_long_posi_con
        print "self.open_short_posi_con:", self.open_short_posi_con
        print "self.delta_open_posi_con:", self.delta_open_posi_con
        
class databaseFUT:
    
    DB_RAW_SUBFILE_NAME = '.stk'
    
    def __init__(self, db_dir, valid_days, type_list):
        self.Info_list = []
        self.Info_hash = {}
        self.VALID_DAYS = valid_days
        self.type_list = type_list
        self.__proc(db_dir)
        pass
    
    def __proc(self, db_dir):
        for type in self.type_list:            
            db_file_list = list_all_file(db_dir, type, self.DB_RAW_SUBFILE_NAME)            
            for dbfile in db_file_list:
                info = FUTInfo(dbfile)
                self.Info_list.append(info)
                self.Info_hash[info.Date] = info
                #info.show()                
            print dbfile
    
##############################################################
# main test
##############################################################

if __name__ == '__main__':
    
    type_list = ['FUT']        
    cfg = config('./config/setting.xml')            
    databaseFUT(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), type_list)    
    
    pass
