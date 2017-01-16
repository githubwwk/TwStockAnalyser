
from htmlParserFG import analyze_fg_html
from htmlParserTWSE import analyze_twse_html
from htmlParserFGMajor import analyze_fgmajor_html
from htmlParserFutures import analyze_futures_html
from database import database
from databaseTWSE import databaseTWSE
from databaseMonitor import databaseMonitor
from databaseFUT import databaseFUT
from config import config 
from reportFG import reportFG
from reportTWSE import reportTWSE
from reportMonitor import reportMonitor
from reportFUT import reportFUT
import utility

##############################################################
# Function
##############################################################
def fg_today_info():
    
    # Get FG daily data
    analyze_fg_html('TSE_FGB', 'https://tw.stock.yahoo.com/d/i/fgbuy_tse50.html')
    analyze_fg_html('TSE_FGS', 'https://tw.stock.yahoo.com/d/i/fgsell_tse50.html')
    analyze_fg_html('OTC_FGB', 'https://tw.stock.yahoo.com/d/i/fgbuy_otc50.html')    
    analyze_fg_html('OTC_FGS', 'https://tw.stock.yahoo.com/d/i/fgsell_otc50.html')
    
def twse_today_info():
    
    # Get TWSE daily data
    analyze_twse_html('TWSE')  
    analyze_fgmajor_html('FG_MAJOR', 'https://tw.stock.yahoo.com/d/i/major.html')

def futures_today_info():
    analyze_futures_html('FUT')    
    
def main():
    
    type_list = ['OTC_FGB', 'OTC_FGS', 'TSE_FGB', 'TSE_FGS']
    twsw_type_list = ['TWSE', 'FG_MAJOR']
    fut_type_list = ['FUT'] 
    cfg = config('./config/setting.xml')
    
    hour = utility.current_hour()
    if (hour >= 15) and (hour < 24):
        # Get today data from network, data valid time 17:00~23:00
        fg_today_info()
        twse_today_info()
        futures_today_info()
        pass
    else:
        #fg_today_info()
        #twse_today_info()
        pass
            
    # Init stock database
    db = database(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), type_list)
    db_twse = databaseTWSE(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), twsw_type_list)
    db_monitor = databaseMonitor(db, cfg)  
    db_futures = databaseFUT(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), fut_type_list)      
    
    # Generate web page        
    reportFG(db, cfg.REPORT_DIR, cfg.TEMPLATE_DIR, type_list) 
    reportTWSE(db_twse, cfg.REPORT_DIR, cfg.TEMPLATE_DIR, twsw_type_list)        
    reportMonitor(db_monitor, cfg.REPORT_DIR, cfg.TEMPLATE_DIR)   
    reportFUT(db_futures, cfg.REPORT_DIR, cfg.TEMPLATE_DIR, fut_type_list)    
    
##############################################################
# main test2l-
##############################################################

if __name__ == '__main__':    
    
    #if utility.is_weekend() == True:
    #    print "INFO - Today is weekend. Exit"
    #    exit(0)
        
    main()
    print "INFO - Done"
    pass  
