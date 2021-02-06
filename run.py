from util.HTMLTestRunner import HTMLTestRunner
from testcases.demo_testcase import DemoTestCase
from util.readconfig import report_path
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
        HTMLTestRunner(stream=fp, verbosity=2, title="测试报告", description="测试案例执行结果").run(suite)


if __name__ == '__main__':
    suite = test_suite()
    run(suite)
