from util.HTMLTestRunner import HTMLTestRunner
from testcases.demo_testcase import DemoTestCase
from util.readconfig import report_path
from util.readconfig import database_connection_url
from util.readconfig import database_user
from util.readconfig import database_password
from util.readconfig import api_url
from util.readconfig import api_key
from util.mylogger import logger
from frozen_path import cur_path
from util.file import mkdir
import unittest
import time
import os
import re


def test_suite():
    cases = unittest.TestLoader().loadTestsFromTestCase(DemoTestCase)
    suite = unittest.TestSuite([cases])
    return suite


def run(suite):
    report = ''
    test_description = "<p>[ORACLE 数据库]</p><p style='text-indent:0.5'><strong>DB_Connection:</strong> {}</p> " \
                       "<p style='text-indent:0.5'><strong>DB_User:</strong> {}</p> " \
                       "<strong><p style='text-indent:0.5'>DB_Password:</strong> {}</p> " \
                       "<br><p>[接口]</p> <p style='text-indent:0.5'><strong>Api:</strong> {}</p> " \
                       "<p style='text-indent:0.5'><strong>Api_Key:</strong> {}</p>"\
                        .format(database_connection_url, database_user, database_password, api_url, api_key)
    cur_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    if report_path is '' or report_path is None:
        project_path = cur_path()
        mkdir(os.path.join(project_path, 'report'))
        report = os.path.join(project_path, 'report', 'ESPOS82_Promotion_AutoTest_{}.html'.format(cur_time))
    elif not report_path.endswith('.html'):
        logger.info('report path: {}配置有误，正确格式如： D:\\report.html'.format(report_path))
        return
    else:
        report = re.sub(r'\.html', '_{}.html'.format(cur_time), report_path)
    with open(report, 'wb') as fp:
        HTMLTestRunner(stream=fp, verbosity=2, title="测试报告", description="", test_description=test_description).run(suite)


if __name__ == '__main__':
    suite = test_suite()
    run(suite)
