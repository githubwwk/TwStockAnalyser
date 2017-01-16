import utility
import os
from config import config 
from database import database
import shutil

class reportFG:
    
    def __init__(self, db, report_repository, template_dir, type_list):
        
        # Create daily report folder
        report_dir = self.__create_report_daily_folder(report_repository)
        
        # Copy template html file.
        self.__copy_template(report_dir, template_dir)
        
        # Generate FG reports
        for report_type in type_list:            
            self.__gen_fg_report(db, report_dir, template_dir, report_type)
        
        pass
    
    def __create_report_daily_folder(self, report_repository):        
        
        report_dir = report_repository + '/' + utility.get_date_str(utility.DATE_STYLE_0)
        report_dir = os.path.abspath(report_dir)        
        if not os.path.exists(report_dir):
                os.makedirs(report_dir)
                print "DEBUG - [Create Report Dir]:", report_dir
        
         
        material_dir = report_dir + '/material'
        if not os.path.exists(material_dir):
                os.makedirs(material_dir)
                print "DEBUG - [Create Report's material Dir]:", material_dir
                            
        return report_dir        
    
    def __copy_template(self, report_dir, template_dir):
        
        # Copy index.html
        src_file = template_dir + '/template__index.html'
        dest_file = report_dir + '/index.html'        
        shutil.copy2(src_file, dest_file)

        # Copy menu.html
        src_file = template_dir + '/template__menu.html'
        dest_file = report_dir + '/material/menu.html'        
        shutil.copy2(src_file, dest_file)
        
        pass
    
    def __gen_fg_report(self, db, report_dir, template_dir, report_type):
        
        file_name = report_dir+ '/material/' + report_type + '_report.html'
        template_file = template_dir + '/' + 'template__fg.html'
                
        report_file = open(file_name, 'w')
        report_template = open(template_file, 'r')

        print "INFO - [Gen FG Report]:", file_name

        for line in report_template:
            if(line.find('@TABLE_TITLE@')>=0):
                caption_html = "<caption>%s Report</caption>" % (report_type)
                report_file.write(caption_html)
            elif(line.find('@TABLE_DATA@')>=0):
                stock_id_list, stock_name_list = db.get_last_stock_info(report_type)                
                for index in range( len(stock_id_list)):
                    stock_id = stock_id_list[index]
                    stock_name = stock_name_list[index]
                    #print "INFO - [stock_id]:", stock_id
                    
                    stock_state = db.get_stock_history(stock_id, database.OUTPUT_HTML_TYPE)
                    
                    html_line = self.__gen_fg_stock_html_content(stock_id, stock_name, stock_state)
                    report_file.write(html_line)                    
                    pass
            else:
                report_file.write(line)
         
        report_file.close()
        report_template.close()        
        pass

    def __gen_fg_stock_html_content(self, stock_id, stock_name, stock_state):
        
        html_line = ''
        link_format_html = "style=\"text-decoration:none\""
        #table_c0_html = "<tr><td width=\"80\"><a " + link_format_html + " href=\"http://tw.stock.yahoo.com/q/ta?s=%s\" target=info> [%s]  -  %s</a></td>"
        table_c0_html = "<tr><td width=\"100\"><a " + link_format_html + " href=\"http://tw.stock.yahoo.com/q/ta?s=%s\" target=\"_new\"> [%s]  -  %s</a></td>"              
        table_c1_html = "<td width=\"1230\">%s</td></tr>"
        
        c0 = table_c0_html % (stock_id, stock_id, stock_name)
        c1 = table_c1_html % (stock_state)
        html_line = c0 + c1 + '\n'
        return html_line
    
##############################################################
# main test
##############################################################

if __name__ == '__main__':
    
    type_list = ['OTC_FGB', 'OTC_FGS', 'TSE_FGB', 'TSE_FGS']        
    cfg = config('./config/setting.xml')    
    db = database(cfg.DATABASE_DIR, int(cfg.VALID_DAYS))
    
    reportFG(db, cfg.REPORT_DIR, cfg.TEMPLATE_DIR, type_list)    
    
    pass
