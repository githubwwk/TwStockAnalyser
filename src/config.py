from xml.etree import ElementTree

class config:
    def __init__(self, xmlfile):
        self.REPORT_DIR = ''
        self.VALID_DAYS = ''
        self.__load(xmlfile)

    def __load(self, xmlfile):
        with open(xmlfile, 'rt') as fxml:
            tree = ElementTree.parse(xmlfile)
            
        # System    
        self.REPORT_DIR = tree.find('./System/REPORT_DIR').get('name')
        self.VALID_DAYS = tree.find('./System/VALID_DAYS').get('name')
        self.DATABASE_DIR = tree.find('./System/DATABASE_DIR').get('name')
        self.TEMPLATE_DIR = tree.find('./System/TEMPLATE_DIR').get('name')
        
        # Monitor
        self.MONITOR_USER      = tree.find('./Monitor/MONITOR_USER').get('name')
        self.MONITOR_LONGTERM  = tree.find('./Monitor/MONITOR_LONGTERM').get('name')
        self.MONITOR_SHORTTERM = tree.find('./Monitor/MONITOR_SHORTTERM').get('name')
        self.MONITOR_SELL      = tree.find('./Monitor/MONITOR_SELL').get('name')
        self.MONITOR_BUY       = tree.find('./Monitor/MONITOR_BUY').get('name')
    
    def show(self):
        print "INFO - REPORT_DIR:", self.REPORT_DIR
        print "INFO - VALID_DAYS:", self.VALID_DAYS
        print "INFO - DATABASE_DIR:", self.DATABASE_DIR
        print "INFO - TEMPLATE_DIR:", self.TEMPLATE_DIR
        
        print "INFO - MONITOR_USER:", self.MONITOR_USER
        print "INFO - MONITOR_LONGTERM:", self.MONITOR_LONGTERM
        print "INFO - MONITOR_SHORTTERM:", self.MONITOR_SHORTTERM
        print "INFO - MONITOR_SELL:", self.MONITOR_SELL
        print "INFO - MONITOR_BUY:", self.MONITOR_BUY
        
        
##############################################################
# main test
##############################################################

if __name__ == '__main__': 
       
    cfg = config('./config/setting.xml')
    cfg.show()
    
    pass
