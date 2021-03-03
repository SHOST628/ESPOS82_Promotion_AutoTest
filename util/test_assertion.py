from util.oracle import oracle
from util.readconfig import totoal_less_error_range
from util.readconfig import detail_less_error_range
from util.param_parser.param_parser import to_dict
from util.param_parser.param_parser import get_param_to_dict
from util.param_parser.param_parser import RESPONSE
from util.case_log import base_log
import json


TOTALCOUNT = 0
DETAILCOUNT = 0
if totoal_less_error_range.strip() == '':
    totoal_less_error_range = 0
if detail_less_error_range.strip() == '':
    detail_less_error_range = 0
totoal_less_error_range = float(totoal_less_error_range)
detail_less_error_range = float(detail_less_error_range)
FLAG = False


class ParamChecker:
    # TODO 解释每个参数，注释判断逻辑
    def param_kd_check(self, test_cls, testcase, response):
        """
        促销参数 KD
        :return:
        """
        pass

    def param_kp_check(self, test_cls, testcase, response):
        pass

    def param_gt_check(self, test_cls, testcase, response):
        pass

    def param_dis_check(self, test_cls, testcase, response):
        """
        【Demo request salesTotal】
        "reqDiscOneItemUserSelect": [
            {
                "promId": "PEOHQO200900006",
                "promMethodId": "1",
                "selectedPromPackages": [
                    {
                        "applySerail": 1,
                        "pkgItems": [
                            {
                                "itemCode": "DS016",
                                "itemOrgId": "000000",
                                "lessItemIndexs": [
                                    {
                                        "lessItemIndex": 0,
                                        "useQty": 1
                                    }
                                ],
                                "pkgQty": 1,
                                "isChecked": true
                            }
                        ]
                    }
                ]
            }
        ]
        【Demo request assertion】
        跟普通case一致
        """
        pass

    def param_xc_check(self, test_cls, testcase, response):
        pass

    def param_xp_check(self, test_cls, testcase, response):
        pass

    def param_xg_check(self, test_cls, testcase, response):
        pass

    def param_nc_check(self, test_cls, testcase, response):
        pass

    def param_bl_check(self, test_cls, testcase, response):
        """
        promid: PEOHQO201100039 ???
        promid: Quota
        加入XE参数
        【request】
        "reqPromQuota": [
            {
                "promId": "PEOHQO201100034",
                "promMethodId": "1",
                "items": [
                    {
                        "itemIndex": 0,
                        "useQty": 1
                    }
                ]
            }
        ]
        【response】
        remainQuota 下存在数据，即通过
        "resPromQuota": [
          "remainQuota":       {
             "memoCount": 99,
             "orgAmount": null,
             "qty": 999,
             "selAmount": 999999
          }
        ]
        """
        res_prom_quota = response['resPromQuota']
        if res_prom_quota is None:
            test_cls.fail('resPromQuota为{}'.format('None'))
        else:
            if res_prom_quota[0]['remainQuota'] is None:
                test_cls.fail('remainQuota为{}'.format('None'))

    def param_br_check(self, test_cls, testcase, response):
        """
        是否加入XE 参数
        promid: PEOHQO201100039
        【request】
        "reqPromBonusRedeem": {
        "method": 2,
        "details": [
            {
                "gradeCenter": "*",
                "bonusCenter": "*",
                "bonus": 90160
            }
        ]
        }
        【response】
         "resSalesItems": [   {
              "resSalesItemConsumes": [
                {
                    "bonusRedeem": 0,
              ]  }
         }]
        """
        bonus_redeem = get_param_to_dict(test_cls, 'PROMPARAM_BR', testcase, RESPONSE, 'bonusRedeem')
        res_sales_items = response['resSalesItems']
        for i, salesitem in enumerate(res_sales_items):
            for j, sales_comsume in enumerate(salesitem['resSalesItemConsumes']):
                if bonus_redeem[i]['response'] is None:
                    if sales_comsume['bonusRedeem'] == 0:
                        if j == len(salesitem['resSalesItemConsumes']) - 1:
                            pass
                    else:
                        test_cls.fail(
                            "{'Result': {'ItemCode': '%s', 'ActualBonusRedeem': %s, 'ExpectedBonusRedeem': %s}}" %
                            (testcase[i]['ITEMCODE'], sales_comsume['bonusRedeem'], bonus_redeem[i]['response']['bonusredeem']))
                else:
                    if float(bonus_redeem[i]['response']['bonusredeem']) != sales_comsume['bonusRedeem']:
                        if j == len(salesitem['resSalesItemConsumes']) - 1:
                            test_cls.fail("{'Result': {'ItemCode': '%s', 'ActualBonusRedeem': %s, 'ExpectedBonusRedeem': %s}}" %
                                          (testcase[i]['ITEMCODE'], sales_comsume['bonusRedeem'], bonus_redeem[i]['response']['bonusredeem']))

    def param_xe_check(self, test_cls, testcase, response):
        """
        promoid: PEOHQO201100036
        【request】
            "salesTotal": {
                "customerCode": "NV02D0130120000007",
                "bonusBalance": [
                    {
                        "vipGradeCenter": "*",
                        "vipBonusCenter": "*"
                    }
                ]
            }

        salesData 下：
        "vipGradeCenter": [
            "*"
        ],
        "vipBonusCenter": "*"

        【response】
        "resSalesItems": [{
            "bonusGive": 15400
        }]
        """
        param_xe = get_param_to_dict(test_cls, 'PROMPARAM_XE', testcase, RESPONSE, 'bonusGive')
        res_sales_items = response['resSalesItems']
        b_log = '【Param_XE_Log】\n'
        FLAG = False
        actual_itemindexs = {}
        for j, sales_items in enumerate(res_sales_items):
            # record the relationship about item index in testcase and itemindex in response
            actual_itemindexs[sales_items['itemIndex']] = j
        for i, sales_item in enumerate(res_sales_items):
            if i in actual_itemindexs:
                if param_xe[i]['response'] is None:
                    if sales_item['bonusGive'] == 0:
                        pass
                    else:
                        test_cls.fail("{'Result': {'ItemCode': '%s', 'ActualBonusGive': %s, 'ExpectedBonusGive': %s}}" %
                                      (testcase[i]['ITEMCODE'], sales_item['bonusGive'], param_xe[i]['response']))
                elif sales_item['bonusGive'] == float(param_xe[i]['response']['bonusgive']):
                    pass
                else:
                    test_cls.fail("{'Result': {'ItemCode': '%s', 'ActualBonusGive': %s, 'ExpectedBonusGive': %s}}" %
                                  (testcase[i]['ITEMCODE'], sales_item['bonusGive'], param_xe[i]['response']['bonusgive']))
            else:
                if param_xe[i]['response'] is None:
                    pass


class Checker:
    def __init__(self, test_cls):
        self.cls = test_cls

    def check(self, caseid, response, prom_param_list):
        global FLAG
        error_range_doc = ''
        testdata_promparam_sql = "select * from testcase where testcaseid = '{}' order by serialno".format(caseid)
        testcase = oracle.dict_fetchall(testdata_promparam_sql)
        prom_param_list = ["param_{}_check".format(prom_param.lower()) for prom_param in prom_param_list]
        self.response = json.loads(response)
        error_code = self.response['errorCode']
        res_sales_items = self.response['resSalesItems']
        if error_code != 0:
            self.cls.fail("【errorMessage】: {}".format(self.response['errorMessage']))
        # todo simplify code
        elif res_sales_items == []:
            for test_row in testcase:
                promless_detail = test_row['PROMLESSDETAIL']
                if promless_detail is None or promless_detail == '':
                    pass
                else:
                    prom_detail_dict = to_dict(self.cls, 'PROMLESSDETAIL', promless_detail)
                    for key, value in prom_detail_dict.items():
                        if type(value) is list:
                            if len(value) > 1:
                                b_log = base_log(self.cls, testcase, self.response)
                                self.cls.fail(b_log)
                        else:
                            if float(value) != 0:
                                b_log = base_log(self.cls, testcase, self.response)
                                self.cls.fail(b_log)
        else:
            actual_itemindexs = {}
            for j, sales_items in enumerate(res_sales_items):
                # record the relationship about item index in testcase and itemindex in response
                actual_itemindexs[sales_items['itemIndex']] = j
            for i, case in enumerate(testcase):
                promless = to_dict(self.cls, 'PROMLESSDETAIL', case['PROMLESSDETAIL'])
                # check itemindex
                expected_promids = []
                actual_promids = []
                if i in actual_itemindexs:
                    # compare actual promids and expected promids
                    if promless is None:
                        expected_promids = None
                    else:
                        expected_promids = list(promless.keys())
                        expected_promids.sort()
                    for item_consumes in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                        actual_promids.append(item_consumes['promId'])
                    actual_promids.sort()
                    if expected_promids is not None:
                        if len(expected_promids) <= len(actual_promids):
                            # deal with the case that one promid will be shown by multi the same promid
                            actual_promids_tmp = list(set(actual_promids))
                            if actual_promids_tmp == expected_promids:
                                # to compare expected promless total with actual promless total
                                # todo promless total error range
                                if case['PROMLESSTOTAL'] == res_sales_items[actual_itemindexs[i]]['promotionLess']:
                                    pass
                                elif abs(case['PROMLESSTOTAL'] - res_sales_items[actual_itemindexs[i]]['promotionLess']) <= abs(totoal_less_error_range):
                                    FLAG = True
                                    error_range_doc = "<br><font color='green' style='font-weight:bold'>实际与期望结果在误差范围内</font>"
                                else:
                                    b_log = base_log(self.cls, testcase, self.response)
                                    self.cls.fail(b_log)
                                actual_promless_detail = {}
                                if expected_promids == actual_promids:
                                    for item_consumes in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                                        promid = item_consumes['promId']
                                        actual_promless_detail[promid] = []
                                        actual_promless_detail[promid].append(item_consumes['lessAmount'])
                                else:
                                    actual_promids = list(set(actual_promids))
                                    for actual_promid in actual_promids:
                                        for item_consume in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                                            if actual_promid == item_consume['promId']:
                                                if actual_promid in list(actual_promless_detail.keys()):
                                                    actual_promless_detail[actual_promid].append(item_consume['lessAmount'])
                                                else:
                                                    actual_promless_detail[actual_promid] = []
                                                    actual_promless_detail[actual_promid].append(item_consume['lessAmount'])

                                for k, v in promless.items():
                                    if type(v) is list:
                                        if len(v) != len(actual_promless_detail[k]):
                                            b_log = base_log(self.cls, testcase, self.response)
                                            self.cls.fail(b_log)
                                        else:
                                            for h, value in enumerate(v):
                                                # todo promless detail  errorrange
                                                if value == actual_promless_detail[k][h]:
                                                    pass
                                                elif abs(value - actual_promless_detail[k][h]) <= \
                                                        abs(detail_less_error_range):
                                                    FLAG = True
                                                    error_range_doc = "<br><font color='green' style='font-weight:bold'>实际与期望结果在误差范围内</font>"
                                                else:
                                                    b_log = base_log(self.cls, testcase, self.response)
                                                    self.cls.fail(b_log)
                                    else:
                                        if len(actual_promless_detail[k]) > 1:
                                            b_log = base_log(self.cls, testcase, self.response)
                                            self.cls.fail(b_log)
                                        else:
                                            if float(v) == actual_promless_detail[k][0]:
                                                pass
                                            elif abs(float(v) - actual_promless_detail[k][0]) <= \
                                                    abs(detail_less_error_range):
                                                FLAG = True
                                                error_range_doc = "<br><font color='green' style='font-weight:bold'>实际与期望结果在误差范围内</font>"
                                            else:
                                                b_log = base_log(self.cls, testcase, self.response)
                                                self.cls.fail(b_log)
                                if i == len(testcase) - 1:
                                    if FLAG:
                                        self.cls._testMethodDoc += error_range_doc
                            # if actual promids and expected promids are not equal,testcase failed
                            else:
                                b_log = base_log(self.cls, testcase, self.response)
                                self.cls.fail(b_log)
                        # if actual promids and expected promids are not equal,testcase failed
                        else:
                            b_log = base_log(self.cls, testcase, self.response)
                            self.cls.fail(b_log)
                    else:
                        # todo error range (total error range)
                        # if promlessdetail in testcase is None, to confirm total promtionless in resonse
                        if res_sales_items[actual_itemindexs[i]]['promotionLess'] == 0:
                            pass
                        elif res_sales_items[actual_itemindexs[i]]['promotionLess'] <= abs(totoal_less_error_range):
                            FLAG = True
                            error_range_doc = "<br><font color='green' style='font-weight:bold'>实际与期望结果在误差范围内</font>"
                            if i == len(testcase) - 1:
                                if FLAG:
                                    self.cls._testMethodDoc += error_range_doc
                        else:
                            b_log = base_log(self.cls, testcase, self.response)
                            self.cls.fail(b_log)
                else:
                    if promless is None:
                        if i == len(testcase) - 1:
                            if FLAG:
                                self.cls._testMethodDoc += error_range_doc
                    # todo
                    else:
                        b_log = base_log(self.cls, testcase, self.response)
                        self.cls.fail(b_log)
        for param in prom_param_list:
            if hasattr(ParamChecker, param):
                param_checker = getattr(ParamChecker, param)
                param_checker(ParamChecker, self.cls, testcase, self.response)
            else:
                self.cls.skipTest('本程序没有设置该促销参数: {} 的判断条件'.format(param))



