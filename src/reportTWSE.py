import utility
import os
from config import config 
from databaseTWSE import databaseTWSE
from databaseTWSE import TWSEInfo
import shutil

class reportTWSE:
    
    def __init__(self, db, report_repository, template_dir, type_list):
        
        # Create daily report folder
        report_dir = self.__create_report_daily_folder(report_repository)
        
        # Copy template html file.
        self.__copy_template(report_dir, template_dir)
        
        # Generate FG reports
        for report_type in type_list:            
            self.__gen_twse_report(db, report_dir, template_dir, report_type)
        
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
    
    def __gen_twse_report(self, db, report_dir, template_dir, report_type):
        
        file_name = report_dir+ '/material/' + report_type + '_report.html'
        template_file = template_dir + '/' + 'template__twse.html'
                
        report_file = open(file_name, 'w')
        report_template = open(template_file, 'r')

        print "INFO - [Gen TWSE Report]:", file_name

        for line in report_template:            
            if(line.find('@TABLE_TITLE@')>=0):                
                caption_html = "<caption>%s Report</caption>" % (report_type)
                report_file.write(caption_html)
            elif(line.find('@TABLE_DATA@')>=0):
                              
                for twse_info in db.TWSEInfo_list:                                   
                    html_line = self.__gen_twse_html_content(twse_info)                    
                    report_file.write(html_line)                    
                    pass
            else:
                report_file.write(line)
         
        report_file.close()
        report_template.close()        
        pass

    def __gen_twse_html_content(self, twse_info):
        
        html_line = ''
        link_format_html = "style=\"text-decoration:none\""
        
        if twse_info.TwADType == '+' or twse_info.TwADType == '＋':
            twAD = '<font color=\"red\" face=\"Arial\">+%s</font>' % twse_info.TwAD            
        elif twse_info.TwADType == '-' or twse_info.TwADType == '－':
            twAD = '<font color=\"green\" face=\"Arial\">-%s</font>' % twse_info.TwAD
        else:
            twAD = '<font color=\"green\" face=\"Arial\">N/A</font>'
        
        twANR = '<font color=\"red\" face=\"Arial\">%s</font>' % twse_info.TwANR
        twDNR = '<font color=\"green\" face=\"Arial\">%s</font>' % twse_info.TwDNR
        
        if '-' in twse_info.FGTSEMajor:
            FGTSEMajor = '<font color=\"green\" face=\"Arial\">%s</font>' % twse_info.FGTSEMajor
        else:
            FGTSEMajor = '<font color=\"red\" face=\"Arial\">%s</font>' % twse_info.FGTSEMajor

        if '-' in twse_info.FGOTCMajor:
            FGOTCMajor = '<font color=\"green\" face=\"Arial\">%s</font>' % twse_info.FGOTCMajor
        else:
            FGOTCMajor = '<font color=\"red\" face=\"Arial\">%s</font>' % twse_info.FGOTCMajor
        
                
        table_content_html = []
        table_content_html.append(("<tr><td width=\"100\">%s</td>") % twse_info.TwDate)
        table_content_html.append(("<td width=\"100\">%s</td>") % twse_info.TwIndex)        
        table_content_html.append(("<td width=\"100\">%s</td>") % twAD)
        table_content_html.append(("<td width=\"100\">%s</td>") % twANR)         
        table_content_html.append(("<td width=\"100\">%s</td>") % twDNR)
        table_content_html.append(("<td width=\"100\">%s</td>") % FGTSEMajor)   
        table_content_html.append(("<td width=\"100\">%s</td></tr>") % FGOTCMajor)           
        for td in table_content_html:            
            html_line += td + '\n'
            
        return html_line
    
##############################################################
# main test
##############################################################

if __name__ == '__main__':
    
    twsw_type_lsit = ['TWSE', 'FG_MAJOR']
    cfg = config('./config/setting.xml')       
    db_twse = databaseTWSE(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), twsw_type_lsit) 
    db_twse = databaseTWSE(cfg.DATABASE_DIR, int(cfg.VALID_DAYS), twsw_type_lsit)  
    reportTWSE(db_twse, cfg.REPORT_DIR, cfg.TEMPLATE_DIR, twsw_type_lsit)    
    
    pass
