from util.ddt import ddt
from util.ddt import data
from util.ddt import unpack
from util.oracle import oracle
from util.mylogger import logger
from util.readconfig import api_key
from util.readconfig import api_url
from util.readconfig import prom_param
from util.readconfig import skip_caseids
from util.readconfig import only_test_caseids
from util.readconfig import exclude_promparam
from param_parser.param_parser import to_dict
from param_parser.param_parser import param_extractors
from param_parser.param_parser import param_extractor
from param_parser.param_parser import exclude_case
from param_parser.param_parser import exclude_param_case
from param_parser.param_parser import only_test_case
from json_producer.assembler import Assembler
from con_requests.send_request import Requester
from util.ddt import TestNameFormat
from testcases.test_assertion import Checker
import unittest
import json
import io


testcase_id_sql = "select distinct testcaseid from testcase order by testcaseid"
testcase_ids = oracle.select(testcase_id_sql)



@ddt(testNameFormat=TestNameFormat.INDEX_ONLY)
class DemoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requester = Requester(cls, api_url, api_key)

    @data(*testcase_ids)
    @unpack
    def test_demo(cls, testcaseid):
        testcase_sql = "select * from testcase where testcaseid = '{}' order by serialno".format(testcaseid)
        testcase = oracle.dict_fetchall(testcase_sql)
        testcase_desci = '【DESCRIPTION】: ' + testcase[0]['TESTCASEDESCI']
        if testcase_desci is None:
            testcase_desci = '【DESCRIPTION】: '
        promparam_desci = ''
        if 'PROMPARAMETER' in testcase[0]:
            for case in testcase:
                if case['PROMPARAMETER'] is not None and case['PROMPARAMETER'] != '':
                    promparam_desci += case['PROMPARAMETER'] + '；&nbsp&nbsp'
        space = '&nbsp'*41
        # testcase_desci = """<br>&nbsp&nbsp{}{} ;<br>{}【PROMPARAMETER】: {}""".format(space, testcase_desci, space, promparam_desci)
        testcase_desci = """{} ;<br>【PROMPARAMETER】: {}""".format(testcase_desci, promparam_desci)
        # testcase_desci = """{} ;""".format(testcase_desci)
        cls._testMethodDoc = testcase_desci
        if only_test_caseids != '':
            only_test_case(cls, testcaseid, only_test_caseids, cls._testMethodDoc)
        elif skip_caseids != '':
            exclude_case(cls, testcaseid, skip_caseids)
        # TODO START CHANGE
        # to extract common promtion param list
        _promless_detail = {}
        prom_param_list = []
        tmp = []
        for case in testcase:
            if case['PROMLESSDETAIL'] != None:
                tmp.append(case['PROMLESSDETAIL'])
        promless_str = ','.join(tmp)
        # _promless_detail['PROMLESSDETAIL'] = promless_str
        tmp = to_dict(cls, 'PROMLESSDETAIL', promless_str)
        if tmp is not None:
            promids = tmp.keys()
            prom_param_list = param_extractors(promids, prom_param)
        else:
            if prom_param_list == []:
                if 'PROMPARAMETER' in testcase[0]:
                    promparam_str = testcase[0]['PROMPARAMETER']
                    prom_param_list = param_extractor(promparam_str, prom_param)
        exclude_param_case(cls, exclude_promparam, prom_param_list)
        # TODO END
        # add description for testcase
        # TODO 增加 promparam description
        # promparam_desci = ''
        # if 'PROMPARAMETER' in testcase[0]:
        #     for desci in testcase:
        #         if desci is not None or desci.stirp() != '':
        #             promparam_desci = desci['PROMPARAMETER']
        # testcase_desci = """{} ;<br>【PROMPARAMETER】: {}""".format(testcase_desci, promparam_desci)
        # # testcase_desci = """{} ;""".format(testcase_desci)
        # cls._testMethodDoc = testcase_desci
        # assemble a complete request json
        assembler = Assembler(cls, testcase, prom_param_list)
        request_json = assembler.assemble()
        res = cls.requester.post(request_json)
        response = ''
        if res.status_code != 200:
            cls.fail('【 response status_code :{}, response text: {} 】'.format(res.status_code, res.text))
        try:
            response = json.dumps(json.loads(res.text), indent=4, ensure_ascii=False)
        except Exception:
            cls.fail('【Response】: {}'.format(res.text))
        logger.info('================================================')
        logger.info('RESPONSE:\n {}'.format(response))
        checker = Checker(cls)
        checker.check(testcaseid, response, prom_param_list)

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()