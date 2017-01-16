import utility
import os
from config import config 
from databaseFUT import databaseFUT
from databaseFUT import FUTInfo
import shutil

class reportFUT:
    
    def __init__(self, db, report_repository, template_dir, type_list):
        
        # Create daily report folder
        report_dir = self.__create_report_daily_folder(report_repository)
        
        # Copy template html file.
        self.__copy_template(report_dir, template_dir)
        
        # Generate FG reports
        for report_type in type_list:            
            self.__gen_report(db, report_dir, template_dir, report_type)
        
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
    
    def __gen_report(self, db, report_dir, template_dir, report_type):
        
        file_name = report_dir+ '/material/' + report_type + '_report.html'
        template_file = template_dir + '/' + 'template__fut.html'
                
        report_file = open(file_name, 'w')
        report_template = open(template_file, 'r')

        print "INFO - [Gen FUT Report]:", file_name

        for line in report_template:            
            if(line.find('@TABLE_TITLE@')>=0):                
                caption_html = "<caption>%s Report</caption>" % (report_type)
                report_file.write(caption_html)
            elif(line.find('@TABLE_DATA@')>=0):
                              
                for info in db.Info_list:                                   
                    html_line = self.__gen_html_content(info)                    
                    report_file.write(html_line)                    
                    pass
            else:
                report_file.write(line)
         
        report_file.close()
        report_template.close()        
        pass

    def __gen_html_content(self, info):
        
        html_line = ''
        link_format_html = "style=\"text-decoration:none\""
        TWFUT_index_updown = ''
        
        if '-' in info.delta_posi_con :
            delta_posi_con = '<font color=\"green\" face=\"Arial\"><b>%s</b></font>' % info.delta_posi_con            
        else:
            delta_posi_con = '<font color=\"red\" face=\"Arial\"><b>+%s</b></font>' % info.delta_posi_con

        if '-' in info.delta_open_posi_con :
            delta_open_posi_con = '<font color=\"green\" face=\"Arial\"><b>%s</b></font>' % info.delta_open_posi_con            
        else:
            delta_open_posi_con = '<font color=\"red\" face=\"Arial\"><b>+%s</b></font>' % info.delta_open_posi_con        
        
        if '▲' in info.TWFUT_index_updown:
            TWFUT_index_updown = '<font color=\"red\" face=\"Arial\"><b>%s</b></font>' % info.TWFUT_index_updown 
        else:
            TWFUT_index_updown = '<font color=\"green\" face=\"Arial\"><b>%s</b></font>' % info.TWFUT_index_updown
            
        short_posi_con = '<font color=\"green\" face=\"Arial\">%s</font>' % info.short_posi_con
        open_short_posi_con = '<font color=\"green\" face=\"Arial\">%s</font>' % info.open_short_posi_con
        long_posi_con = '<font color=\"red\" face=\"Arial\">%s</font>' % info.long_posi_con
        open_long_posi_con = '<font color=\"red\" face=\"Arial\">%s</font>' % info.open_long_posi_con
                    
        table_content_html = []
        table_content_html.append(("<tr><td width=\"100\">%s</td>") % info.Date)
        
        table_content_html.append(("<td width=\"100\">%s</td>") % long_posi_con)        
        table_content_html.append(("<td width=\"100\">%s</td>") % short_posi_con)
        table_content_html.append(("<td width=\"100\">%s</td>") % delta_posi_con)         
        table_content_html.append(("<td width=\"100\">%s</td>") % open_long_posi_con)
        table_content_html.append(("<td width=\"100\">%s</td>") % open_short_posi_con)   
        table_content_html.append(("<td width=\"100\">%s</td>") % delta_open_posi_con)
        print "#####", info.TWFUT_name, info.TWFUT_index, info.TWFUT_index_updown
        table_content_html.append(("<td width=\"100\">%s</td>") % info.TWFUT_name)
        table_content_html.append(("<td width=\"120\">%s</td>") % info.TWFUT_index)
        table_content_html.append(("<td width=\"120\">%s</td></tr>") % TWFUT_index_updown)
                           
        for td in table_content_html:            
            html_line += td + '\n'
            
        return html_line
    
##############################################################
# main test
##############################################################

if __name__ == '__main__':
    
    type_lsit = ['FUT']
    cfg = config('./config/setting.xml')       
    db_fut = databaseFUT(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), type_lsit)  
    reportFUT(db_fut, cfg.REPORT_DIR, cfg.TEMPLATE_DIR, type_lsit)    
    
    pass
