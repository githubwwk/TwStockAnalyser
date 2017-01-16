import os
from config import config 
from utility import read_file
from utility import list_all_file

##############################################################
# FGMAJORInfo
##############################################################
class FGMAJORInfo:
    VALID_DATA_NR = 4
    def __init__(self, dbfile):
        self.TwDate = ''
        self.FGOTCMajor = ''
        self.FGTSEMajor = ''
        self.__load(dbfile)
        pass

    def __load(self, dbfile):
        file_data = read_file(dbfile)
        data_list = file_data.split(';')
       
        if (len(data_list) != self.VALID_DATA_NR):
            print "ERROR - Invalid TWSE DB content." 
        else:
            self.TwDate   = data_list[0] 
            self.FGTSEMajor = data_list[1]  # FG TSE Major 
            self.FGOTCMajor = data_list[2]  # FG OTC Major           
            print self.FGTSEMajor 
            print self.FGOTCMajor            
        pass    
    
##############################################################
# TWSEInfo
##############################################################
class TWSEInfo:
    
    VALID_DATA_NR = 7
    
    def __init__(self, dbfile):
        self.TwDate = ''
        self.TwIndex = ''  # TSE Index
        self.TwADType = '' # AD Type, +/-
        self.TwAD = ''     # AD: Advance-Decline
        self.TwANR = ''    #Advances Declines
        self.TwDNR = ''    # Declines Number
        
        self.FGOTCMajor = ''
        self.FGTSEMajor = ''
        
        self.__load(dbfile)
        pass

    def __load(self, dbfile):
        file_data = read_file(dbfile)
        data_list = file_data.split(';')
       
        if (len(data_list) != self.VALID_DATA_NR):
            print "ERROR - Invalid TWSE DB content." 
        else:
            self.TwDate   = data_list[0] 
            self.TwIndex  = data_list[1]  # TSE Index
            self.TwADType = data_list[2]  # AD Type, +/-
            self.TwAD  = data_list[3]     # AD: Advance-Decline
            self.TwANR = data_list[4]     #Advances Declines
            self.TwDNR = data_list[5]     # Declines Number
            
            b = map(ord, self.TwADType)   # String to Byte
            if (b[1] == 207):
                self.TwADType = '+'
            elif (b[1] == 208):     
                self.TwADType = '-'
            else:
                print "ERROR - Invalid TwADType Data:", self.TwADType   
        pass

    def show(self):
        print "self.TwDate:", self.TwDate
        print "self.TwIndex:", self.TwIndex
        print "self.TwADType:", self.TwADType
        print "self.TwAD:", self.TwAD 
        print "self.TwANR:", self.TwANR
        print "self.TwDNR:", self.TwDNR
        
class databaseTWSE:
    
    DB_RAW_SUBFILE_NAME = '.stk'
    
    def __init__(self, db_dir, valid_days, type_list):
        self.TWSEInfo_list = []
        self.TWSEInfo_hash = {}
        self.VALID_DAYS = valid_days
        self.type_list = type_list
        self.__proc(db_dir)
        pass
    
    def __proc(self, db_dir):
        for type in self.type_list:            
            db_file_list = list_all_file(db_dir, type, self.DB_RAW_SUBFILE_NAME)            
            for dbfile in db_file_list:
                
                if type == 'TWSE':
                    twseInfo = TWSEInfo(dbfile)
                    self.TWSEInfo_list.append(twseInfo)
                    self.TWSEInfo_hash[twseInfo.TwDate] = twseInfo
                elif type == 'FG_MAJOR':
                    fgmjrInfo = FGMAJORInfo(dbfile)
                    try:
                        twseInfo = self.TWSEInfo_hash[fgmjrInfo.TwDate]
                        twseInfo.FGOTCMajor = fgmjrInfo.FGOTCMajor
                        twseInfo.FGTSEMajor = fgmjrInfo.FGTSEMajor
                    except:
                        print "ERROR - W/o twseInfo in hash. (%s)" % fgmjrInfo.TwDate 
                    pass
                #twseInfo.show()
                print dbfile
    
##############################################################
# main test
##############################################################

if __name__ == '__main__':
    
    type_list = ['TWSE']        
    cfg = config('./config/setting.xml')            
    databaseTWSE(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), type_list)    
    
    pass
