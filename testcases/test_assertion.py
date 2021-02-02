from util.oracle import oracle
from util.readconfig import totoal_less_error_range
from util.readconfig import detail_less_error_range
from param_parser.param_parser import to_dict
from param_parser.param_parser import get_param_to_dict
from param_parser.param_parser import RESPONSE
from param_parser.param_parser import REQUEST
from util.logger import logger
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
        res_prom_quota = testcase['resPromQuota']


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
        for i, sales_item in enumerate(res_sales_items):
            print(param_xe)
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


class Checker:
    def __init__(self, test_cls):
        self.cls = test_cls

    def check(self, caseid, response, prom_param_list):
        global TOTALCOUNT
        global DETAILCOUNT
        global FLAG
        testdata_promparam_sql = "select * from testcase where testcaseid = '{}' order by serialno".format(caseid)
        testcase = oracle.dict_fetchall(testdata_promparam_sql)
        prom_param_list = ["param_{}_check".format(prom_param.lower()) for prom_param in prom_param_list]
        self.response = json.loads(response)
        error_code = self.response['errorCode']
        res_sales_items = self.response['resSalesItems']
        if error_code != 0:
            self.cls.fail("【errorMessage】: {}".format(self.response['errorMessage']))
        elif res_sales_items == []:
            for test_row in testcase:
                promless_detail = test_row['PROMLESSDETAIL']
                if promless_detail is None:
                    pass
                else:
                    prom_detail_dict =  to_dict(self.cls, 'PROMLESSDETAIL', promless_detail)
                    for key, value in prom_detail_dict.items():
                        if float(value) != 0:
                            # self.cls.fail("【Actual Result】: 不中促销； 【Expected Result】: {}".format(promless_detail))
                            self.cls.fail("{'Result: { {'ItemCode': %s, 'Actual ': 不中促销, 'Expected PromlessDetail': %s } } }" %
                                          (test_row['ITEMCODE'], promless_detail))
        else:
            for i, salesitem in enumerate(res_sales_items):
                item_index = salesitem['itemIndex']
                actual_total_promless = salesitem['promotionLess']
                expected_total_promless = testcase[item_index]['PROMLESSTOTAL']
                if expected_total_promless is None:
                    expected_total_promless = 0
                if expected_total_promless is None:
                    if i == len(res_sales_items) - 1:
                        if TOTALCOUNT == i:
                            TOTALCOUNT = 0
                            self.cls.skipTest('请补充【TestCase】下 PROMLESSTOTAL 的数据')
                    TOTALCOUNT += 1
                # if actual total promotionLess != expected total promotionLess, testcase failed
                if abs(actual_total_promless - expected_total_promless) <= abs(totoal_less_error_range):
                    if abs(actual_total_promless - expected_total_promless) != 0:
                        FLAG = True
                    res_salesitem_consumes = salesitem['resSalesItemConsumes']
                    # TODO promotionLess detail
                    expected_promotionless_detail = to_dict(self.cls, 'PROMLESSDETAIL', testcase[item_index]['PROMLESSDETAIL'])
                    if expected_promotionless_detail is None:
                        if i == len(res_sales_items) - 1:
                            if DETAILCOUNT == i:
                                DETAILCOUNT = 0
                                self.cls.skipTest('请补充【TestCase】下 PROMLESSDETAIL 的数据')
                        DETAILCOUNT += 1
                    for j, salesitem_consume in enumerate(res_salesitem_consumes):
                        res_prom_id = res_salesitem_consumes[j]['promId']
                        # if actual promid is not in expected promid list, testcase failed. In addition, if expected promid list is None, need to add something to it
                        if expected_promotionless_detail is None:
                            expected_promotionless_detail = {res_prom_id: 0}
                        if res_prom_id not in expected_promotionless_detail:
                            self.cls.fail("Actual PromId 不在 Expected PromId 列表中: {}".format(testcase[item_index]['PROMLESSDETAIL']))
                        else:
                            # if detail lessAmount is not equal to detail expected promotionless, testcase failed
                            if abs(float(expected_promotionless_detail[res_prom_id]) - salesitem_consume['lessAmount']) > abs(detail_less_error_range):
                                self.cls.fail(
                                    "{ 'Result': {'ItemCode': '%s', 'PromLessDetail':{ {'PromId': '%s', 'ActualLessAmount': %s,  'ExpectedLessAmount': %s} } } }" %
                                    (testcase[item_index]['ITEMCODE'], res_prom_id, salesitem_consume['lessAmount'], expected_promotionless_detail[res_prom_id]))
                            elif abs(float(expected_promotionless_detail[res_prom_id]) - salesitem_consume['lessAmount']) != 0:
                                FLAG = True
                            if i == len(res_sales_items) - 1:
                                if j == len(res_salesitem_consumes) -1:
                                    if FLAG:
                                        FLAG = False
                                        self.cls._testMethodDoc += ' ; PromotionLess 在误差范围内'
                else:
                    self.cls.fail("{ 'Result': {'ItemCode': '%s', 'PromLessTotal':{'ActualLessAmount': %s,  'ExpectedLessAmount': %s}} }" %
                                  (testcase[item_index]['ITEMCODE'], actual_total_promless, expected_total_promless))
        for param in prom_param_list:
            if hasattr(ParamChecker, param):
                param_checker = getattr(ParamChecker, param)
                param_checker(ParamChecker, self.cls, testcase, self.response)
            else:
                self.cls.skipTest('本程序没有设置该促销参数: {} 的判断条件'.format(param))



