from configparser import ConfigParser
from frozen_path import cur_path
import os


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
project_path = cur_path()

#  TODO 加入异常处理 ? key 不存在 和 读取错误
config_path = os.path.join(project_path, 'config\\config.ini')
config = ConfigParser()
config.read(config_path, encoding='utf-8-sig')

# DB config
database_connection_url = config.get('DataSource', 'DatabaseConnectionUrl')
database_user = config.get('DataSource', 'DatabaseUser')
database_password = config.get('DataSource', 'DatabasePassword')
db_type = config.get('DataSource','Mysql_Oracle_Connection')
db_url = database_user + '/' + database_password + '@' + database_connection_url

# api
api_url = config.get('Api', 'Url')
api_key = config.get('Api', 'ApiKey')

# JsonModel
base_json = config.get('JsonModel', 'BaseJson')

#JsonConfig
request_now = config.get('JsonConfig','RequestNow')

# PromParams
prom_param = config.get('PromParams', 'PromParam')
exclude_promparam = config.get('PromParams', 'ExcludePromParam')
br_method_id = config.get('PromParams', 'BRMethodId')
bl_method_id = config.get('PromParams', 'BLMethodId')
dis_method_id = config.get('PromParams', 'DISMethodId')
kp_method_id = config.get('PromParams', 'KPMethodId')

# PromSalesItemDefault
invt_type = config.get('PromSalesItemDefault', 'invtType')
price_mode = config.get('PromSalesItemDefault', 'priceMode')
disc_mode = config.get('PromSalesItemDefault', 'discMode')
disc_value = config.get('PromSalesItemDefault', 'discValue')
itemlot_num = config.get('PromSalesItemDefault', 'itemLotNum')

#  reqDiscOneItemUserSelectDefault
apply_serail = config.get('reqDiscOneItemUserSelectDefault', 'applySerail')
is_checked =  config.get('reqDiscOneItemUserSelectDefault', 'isChecked')

# TestCaseParam
# totoal_less_error_range = config.get('TestCaseParam', 'TotoalLessErrorRange')  # deprecated
detail_less_error_range = config.get('TestCaseParam', 'DetailLessErrorRange')
skip_caseids = config.get('TestCaseParam', 'SkipCaseId')
only_test_caseids = config.get('TestCaseParam', 'OnlyTestCaseId')
approximate_matching = config.get('TestCaseParam', 'ApproximateMatching')


# report path
html_excel = config.get('Report', 'Html_Excel')
report_path = config.get('Report', 'Path')

# email config
if_send = config.get("Mail", "If_Send")
email_host = config.get("Mail", "Host")
email_user = config.get("Mail", "User")
email_psw = config.get("Mail", "Psw")
Receivers = config.get("Mail", "Receivers")

# Log
log_file = config.get('Log', 'LogFile')
debug_level = config.get('Log', 'DebugLevel')






