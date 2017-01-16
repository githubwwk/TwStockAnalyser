from xml.etree import ElementTree
from config import config
from database import database


##############################################################
# StockInfo
##############################################################
class StockInfo:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.price = ''
        self.date = ''
        self.type = ''
        self.note = '' 
        self.state = ''
    def show(self):
        print "id:", self.id
        print "name:", self.name
        print "price:", self.price
        print "date:", self.date
        print "type:", self.type
        print "note:", self.note
        print "state:", self.state            
        
             
##############################################################
# Monitor
##############################################################
class Monitor():
    def __init__(self, type):
        self.type = type
        self.stockInfoList = []     
        pass
    
    
##############################################################
# databaseMonitor
##############################################################                    
class databaseMonitor:
    def __init__(self, db, cfg):
        
        self.monitor_list = []
        self.monitor_type_hash = {}        
                
        self.__load_monitor_type(cfg)
        
        for type, cfg_file in self.monitor_type_hash.iteritems():
            if cfg_file != '':
                print "@@@", cfg_file
                self.__load(type, cfg_file, db)
        pass
    
    def __load_monitor_type(self, cfg):        
        # Assign monitor configuration file to hash.
        self.monitor_type_hash['MONITOR_USER'] = cfg.MONITOR_USER
        self.monitor_type_hash['MONITOR_LONGTERM'] = cfg.MONITOR_LONGTERM
        self.monitor_type_hash['MONITOR_SHORTTERM'] = cfg.MONITOR_SHORTTERM
        self.monitor_type_hash['MONITOR_BUY'] = cfg.MONITOR_BUY
        self.monitor_type_hash['MONITOR_SELL'] = cfg.MONITOR_SELL            
    
    def __load(self, type, xmlfile, db):
        
        monitor = Monitor(type)
        
        with open(xmlfile, 'rt') as fxml:
            tree = ElementTree.parse(fxml)
        
        #Get all monitor stock information     
        for stock in tree.findall('./Stock'):
            stockInfo = StockInfo()
            stockInfo.id = stock.get('id').encode('big5')
            stockInfo.name = stock.get('name').encode('big5')
            stockInfo.price = stock.get('price').encode('big5')
            stockInfo.date = stock.get('date').encode('big5')
            stockInfo.type = stock.get('type').encode('big5')
            stockInfo.node = stock.get('note').encode('big5')
            stockInfo.state = db.get_stock_history(stockInfo.id, database.OUTPUT_HTML_TYPE)       
            stockInfo.show()            
            monitor.stockInfoList.append(stockInfo)
            
        self.monitor_list.append(monitor)
        
##############################################################
# main test
##############################################################

if __name__ == '__main__':
    
    cfg = config('./config/setting.xml')
    type_list = ['OTC_FGB', 'OTC_FGS', 'TSE_FGB', 'TSE_FGS']
    db = database(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), type_list)
    
    databaseMonitor(db, cfg)
    pass
